import pygame
import random
import time
import os
pygame.init()

displayHeight = 600
displayWidth = 800
gameDisplay = pygame.display.set_mode((displayWidth, displayHeight))
pygame.display.set_caption('FlapPy Game')

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

    def hit(self, pipe, displayHeight):
        if pipe != None:
            if player.x + player.width > pipe.x and player.y + player.height > pipe.y or\
            player.x + player.width > pipe.x and player.y < pipe.y - pipe.gap:
                return True
            else:
                return False

        if player.y > displayHeight - player.height:
            return True


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


def redrawDisplay():

    gameDisplay.blit(bg, (0, 0))

    player.draw(gameDisplay)

    for pipe in pipes:
        pipe.draw(gameDisplay)
    score = font.render('Points: ' + str(player.getPoints()), 1, (0,0,0))
    gameDisplay.blit(score, (350,30))
    pygame.display.update()


def deathScreen():
    gameDisplay.blit(bg, (0, 0))

    player.draw(gameDisplay)

    for pipe in pipes:
        pipe.draw(gameDisplay)

    score = font.render('RIP, Points: ' + str(player.getPoints()), 2, (0,0,0))
    message = font.render('Press any key to quit.', 2, (0,0,0))

    gameDisplay.blit(score, (displayWidth // 2 - score.get_rect().width // 2, displayHeight // 2 - score.get_rect().height // 2))
    gameDisplay.blit(message, (displayWidth // 2 - message.get_rect().width // 2, displayHeight // 2 - message.get_rect().height // 2 - score.get_rect().height))

    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                return



player = Bird(50, 400, 40, 28)

pipeHeight, pipeWidth, pipeGap = Pipe(0, 0).getAttributes()
pipeCount = 0
pipes = []
font = pygame.font.SysFont('helvetica', 30, True)

run = True
passedPipe = False

while run:
    pygame.time.delay(10)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    drawHeight = random.randint(displayHeight - pipeHeight, pipeHeight + pipeGap)
    if pipeCount == 100:
        pipeCount = 0
        newPipe = Pipe(800, drawHeight, pipeHeight, pipeWidth, pipeGap)
        pipes.append(newPipe)


    keys = pygame.key.get_pressed()

    if player.isJumping:
        if player.jumpCount >= -2:
            neg = 1
            if player.jumpCount < 0:
                neg = -1
            player.y -= 0.3 * player.jumpCount ** 2 * neg
            player.jumpCount -= 1

        else:
            player.jumpCount = 10
            player.isJumping = False

    else:
        if keys[pygame.K_SPACE]:
            player.isJumping = True



    player.y += player.gravity
    pipeCount += 1



    for i, pipe in enumerate(pipes):
        pipe.move()
        pipes[i] = pipe


        if pipe.x + pipe.width // 2 < player.x + player.width < pipe.x + pipe.width // 2 + 2:
            player.addPoint()

    targetPipe = next((pipe for pipe in pipes if pipe.x + pipe.width > player.x), None)



    if player.hit(targetPipe, displayHeight):
        run = False

    if len(pipes) > 0 and pipes[0].outOfFrame():
        pipes.pop(0)


    redrawDisplay()


deathScreen()
pygame.quit()
