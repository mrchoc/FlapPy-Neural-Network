import pygame
import random
import time
import os
import neat


pygame.init()

displayHeight = 600
displayWidth = 800
gameDisplay = pygame.display.set_mode((displayWidth, displayHeight))
pygame.display.set_caption('FlapPy Machine Learning')

current_path = os.path.dirname(__file__) # Where your .py file is located
images_path = os.path.join(current_path, 'images')

bg = pygame.image.load(os.path.join(images_path, 'bg.png'))




class Bird():
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 3
        self.jumpCount = 10
        self.isJumping = False
        self.gravity = 5
        self.points = 0

    def draw(self, gameDisplay):
        bird = pygame.image.load(os.path.join(images_path, 'bird.png'))
        gameDisplay.blit(bird, (self.x, self.y))

    def addPoint(self):
        self.points += 1

    def hitPipe(self, pipe):
        if pipe != None:
            if self.x + self.width > pipe.x and self.y + self.height > pipe.y or\
            self.x + self.width > pipe.x and self.y < pipe.y - pipe.gap:
                return True
            else:
                return False


    def jump(self):
        neg = 1
        if self.jumpCount < 0:
            neg = -1
        self.y -= 0.3 * self.jumpCount ** 2 * neg
        self.jumpCount -= 1




    def getPoints(self):
        return self.points

class Pipe():
    def __init__(self, x, y, height = 301, width = 84, gap = 150):
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.gap = gap
        self.vel = 3


    def draw(self, gameDisplay):
        topPipe = pygame.image.load(os.path.join(images_path, 'topPipe.png'))
        bottomPipe = pygame.image.load(os.path.join(images_path, 'bottomPipe.png'))
        gameDisplay.blit(topPipe, (self.x, self.y - self.height - self.gap))
        gameDisplay.blit(bottomPipe, (self.x, self.y))

    def move(self):
        self.x -= self.vel

    def outOfFrame(self):
        if self.x < -85:
            return True

        else:
            return False

    def getAttributes(self):
        return self.height, self.width, self.gap


def redrawDisplay(players, pipes, font):

    gameDisplay.blit(bg, (0, 0))
    for player in players:
        player.draw(gameDisplay)

    for pipe in pipes:
        pipe.draw(gameDisplay)

    remaining = font.render('Remaining: ' + str(len(players)), 1, (0,0,0))

    gameDisplay.blit(remaining, (600, 20))

    pygame.display.update()




def main(genomes, config):
    nets = []
    ge = []
    players = []

    for _, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        players.append(Bird(50, 400, 40, 28))
        g.fitness = 0
        ge.append(g)



    pipeCount = 100
    pipes = []

    font = pygame.font.SysFont('helvetica', 25, True)

    run = True
    passedPipe = False
    pipeHeight, pipeWidth, pipeGap = Pipe(0, 0).getAttributes()

    while run:
        pygame.time.delay(10)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

        drawHeight = random.randint(displayHeight - pipeHeight, pipeHeight + pipeGap)
        if pipeCount == 100:
            pipeCount = 0
            newPipe = Pipe(800, drawHeight, pipeHeight, pipeWidth, pipeGap)
            pipes.append(newPipe)







        pipeCount += 1



        for i, pipe in enumerate(pipes):
            pipe.move()
            pipes[i] = pipe




        for i, player in enumerate(players):
            player.y += player.gravity
            targetPipe = next((pipe for pipe in pipes if pipe.x + pipe.width > player.x), None)

            if pipe.x + pipe.width // 2 < player.x + player.width // 2 < pipe.x + pipe.width // 2 + 5:
                player.addPoint()
                for g in ge:
                    g.fitness += 5

            ge[i].fitness += 0.1

            output = nets[i].activate((player.y, abs(player.y - targetPipe.height), abs(player.y - targetPipe.y)))

            if output[0] > 0.5:
                if player.jumpCount >= -2:
                    player.jump()

                else:
                    player.jumpCount = 10
                    player.isJumping = False


            if player.hitPipe(targetPipe):
                ge[i].fitness -= 1
                players.pop(i)
                nets.pop(i)
                ge.pop(i)





        if len(pipes) > 0 and pipes[0].outOfFrame():
            pipes.pop(0)

        for i, player in enumerate(players):
            if player.y > displayHeight - player.height or player.y < 0:
                 players.pop(i)
                 nets.pop(i)
                 ge.pop(i)

        if len(players) < 1:
            run = False

        redrawDisplay(players, pipes, font)







def run(config_path):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_path)

    p = neat.Population(config)

    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    winner = p.run(main, 300)



if __name__ == '__main__':
    config_path = os.path.join(current_path, 'config-feedforward.txt')
    run(config_path)
