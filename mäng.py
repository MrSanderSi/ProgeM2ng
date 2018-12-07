import pygame
import os
pygame.init()
screenWidth = 800
screenHeight = 500
win = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption("First Game")
walkRight = [pygame.image.load(os.path.join('character', 'R1.png')) ,pygame.image.load(os.path.join('character', 'R2.png')) ,pygame.image.load(os.path.join('character', 'R3.png')) ,pygame.image.load(os.path.join('character', 'R4.png')) ,pygame.image.load(os.path.join('character', 'R5.png')) ,pygame.image.load(os.path.join('character', 'R6.png'))]
walkLeft = [pygame.image.load(os.path.join('character', 'L1.png')) ,pygame.image.load(os.path.join('character', 'L2.png')) ,pygame.image.load(os.path.join('character', 'L3.png')) ,pygame.image.load(os.path.join('character', 'L4.png')) ,pygame.image.load(os.path.join('character', 'L5.png')) ,pygame.image.load(os.path.join('character', 'L6.png'))]
#walkRight = [pygame.image.load('character/R1.png'),pygame.image.load('character/R2.png'),pygame.image.load('character/R3.png'),pygame.image.load('character/R4.png'),pygame.image.load('character/R5.png'),pygame.image.load('character/R6.png')]
#walkLeft = [pygame.image.load('character/L1.png'),pygame.image.load('character/L2.png'),pygame.image.load('character/L3.png'),pygame.image.load('character/L4.png'),pygame.image.load('character/L5.png'),pygame.image.load('character/L6.png')]
bg = pygame.image.load('background/back.png')
idle = [pygame.image.load('character/idle1.png'),pygame.image.load('character/idle2.png'),pygame.image.load('character/idle3.png'),pygame.image.load('character/idle4.png'),pygame.image.load('character/idle5.png'),pygame.image.load('character/idle6.png'),]
clock = pygame.time.Clock()

class player(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 6
        self.isJump = False
        self.jumpCount = 10
        self.left = False
        self.right = False
        self.idle = True
        self.walkCount = 0
        self.idleCount = 0

    def draw(self,win):
        if self.walkCount + 1 >= 30:
            self.walkCount = 0
        elif self.idleCount + 1 >= 60:
            self.idleCount = 0
        if not(self.idle):
            if self.right:
                win.blit(walkRight[self.walkCount//5], (self.x,self.y))
                self.walkCount += 1
            if self.left:
                win.blit(walkLeft[self.walkCount//5], (self.x,self.y))
                self.walkCount += 1
        else:
            if self.idle:
                win.blit(idle[self.idleCount//10], (self.x,self.y))
                self.idleCount += 1

class projectile(object):
    def __init__(self,x,y,radius,color,facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.vel = 12 * facing
    def draw(self,win):
        pygame.draw.circle(win, self.color, (self.x,self.y), self.radius)

def redrawGameWindow():
    global idleCount
    global walkCount

    win.blit(bg, (0,0))
    fox.draw(win)
    for bullet in bullets:
        bullet.draw(win)
    pygame.display.update()
#MAINLOOP
fox = player(200, 300, 32, 32)
bullets = []
run = True
while run:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    for bullet in bullets:
        if bullet.x < 800 and bullet.x > 0:
            bullet.x += bullet.vel
        else:
            bullets.pop(bullets.index(bullet))

    keys = pygame.key.get_pressed()

    if keys[pygame.K_SPACE]:
        if fox.left:
            facing = -1
        else:
            facing = 1
        if len(bullets) < 1:
            bullets.append(projectile(round(fox.x + fox.width//2), round(fox.y + fox.height//2), 2, (0,0,0), facing))
    if keys[pygame.K_LEFT] and fox.x > fox.vel:
        fox.x -= fox.vel
        fox.left = True
        fox.right = False
        fox.idle = False

    elif keys[pygame.K_RIGHT] and fox.x < screenWidth - fox.width:
        fox.x += fox.vel
        fox.left = False
        fox.right = True
        fox.idle = False
    else:
        fox.right = False
        fox.left = False
        fox.walkCount = 0
        fox.idle = True
    if not (fox.isJump):
        if keys[pygame.K_UP] and fox.y > fox.vel:
            fox.isJump = True
            fox.left = False
            fox.right = False
            fox.idle = False
            fox.walkCount = 0

    else:
        if fox.jumpCount >= -10:
            neg = 1
            if fox.jumpCount < 0:
                neg = -1
            fox.y -= (fox.jumpCount ** 2) * 0.3 * neg
            fox.jumpCount -= 1
        else:
            fox.isJump = False
            fox.jumpCount = 10

    redrawGameWindow()

pygame.quit()
