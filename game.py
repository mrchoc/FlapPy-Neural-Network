import pygame
import random
import time
pygame.init()

displayHeight = 600
displayWidth = 800
gameDisplay = pygame.display.set_mode((displayWidth,displayHeight))
pygame.display.set_caption('FlapPy Game')
bg = pygame.image.load('bg.png')




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
        bird = pygame.image.load('bird.png')
        gameDisplay.blit(bird, (self.x, self.y))
    
    def addPoint(self):
        self.points += 1

    def hit(self):
        return False

    def getPoints(self):
        return self.points

class Pipe():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.height = 301
        self.width = 84
        self.gap = 150
        self.vel = 3

    def draw(self, gameDisplay):
        topPipe = pygame.image.load('topPipe.png')
        bottomPipe = pygame.image.load('bottomPipe.png')
        gameDisplay.blit(topPipe, (self.x, self.y - self.height - self.gap))
        gameDisplay.blit(bottomPipe, (self.x, self.y))

    def move(self):
        self.x -= self.vel

    def outOfFrame(self):
        if self.x < -85:
            return True

        else:
            return False




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
    
    gameDisplay.blit(score, (350,300))
    gameDisplay.blit(message, (350, 270))
    
    pygame.display.update()
    time.sleep(2)
    
    while True:
        if pygame.event.wait() != None:
            return

        

player = Bird(50, 400, 40, 28)
pipeCount = 0
pipes = []
font = pygame.font.SysFont('helvetica', 30, True)
popFirst = False
run = True
passedPipe = False

while run:
    pygame.time.delay(10)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    drawHeight = random.randint(300, 450)
    if pipeCount == 100:
        pipeCount = 0
        newPipe = Pipe(800, drawHeight)
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
    


    for i in range(len(pipes)):
        pipe = pipes[i]
        pipe.move()
        pipes[i] = pipe
        
        if player.x + player.width > pipe.x and player.y + player.height > pipe.y or\
        player.x + player.width > pipe.x and player.y < pipe.y - pipe.gap or\
        player.y > displayHeight:
            run = player.hit()


        elif pipe.x + pipe.width // 2 < player.x + player.width < pipe.x + pipe.width // 2 + 2:
            player.addPoint()

    if len(pipes) > 0 and pipes[0].outOfFrame():
        pipes.pop(0)

    redrawDisplay()


deathScreen()
pygame.quit()
