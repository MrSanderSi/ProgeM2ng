from tileset import *
import pygame
import os
pygame.init()
screenWidth = 800
screenHeight = 500
win = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption("First Game")
walkRight = [pygame.image.load(os.path.join('character', 'R1.png')) ,pygame.image.load(os.path.join('character', 'R2.png')) ,pygame.image.load(os.path.join('character', 'R3.png')) ,pygame.image.load(os.path.join('character', 'R4.png')) ,pygame.image.load(os.path.join('character', 'R5.png')) ,pygame.image.load(os.path.join('character', 'R6.png'))]
walkLeft = [pygame.image.load(os.path.join('character', 'L1.png')) ,pygame.image.load(os.path.join('character', 'L2.png')) ,pygame.image.load(os.path.join('character', 'L3.png')) ,pygame.image.load(os.path.join('character', 'L4.png')) ,pygame.image.load(os.path.join('character', 'L5.png')) ,pygame.image.load(os.path.join('character', 'L6.png'))]
bg = pygame.image.load('background/back.png')
fg = pygame.image.load('background/fg.png')
idle = [pygame.image.load('character/idle1.png'),pygame.image.load('character/idle2.png'),pygame.image.load('character/idle3.png'),pygame.image.load('character/idle4.png'),pygame.image.load('character/idle5.png'),pygame.image.load('character/idle6.png'),]
clock = pygame.time.Clock()
pilv1 = pygame.image.load('background/pilv1.png')
pilv2 = pygame.image.load('background/pilv2.png')

class cloud(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vel = 1
        self.right = True
        self.left = False
        
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
        self.hitbox = (self.x + 2, self.y + 5, 24, 30)

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
        self.hitbox = (self.x + 2, self.y + 5, 24, 30)
        pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)

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

class enemy(object):
    walkRight = [pygame.image.load(os.path.join('eagle', 'eagle-R.png')), pygame.image.load(os.path.join('eagle', 'eagle-R2.png')), pygame.image.load(os.path.join('eagle', 'eagle-R3.png')), pygame.image.load(os.path.join('eagle', 'eagle-R4.png'))]
    walkLeft = [pygame.image.load(os.path.join('eagle', 'eagle-attack-1.png')), pygame.image.load(os.path.join('eagle', 'eagle-attack-2.png')), pygame.image.load(os.path.join('eagle', 'eagle-attack-3.png')), pygame.image.load(os.path.join('eagle', 'eagle-attack-4.png'))]


    def __init__(self, x, y, width, height, end):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.end = end
        self.path = [self.x, self.end]
        self.walkCount = 0
        self.vel = 3
        self.hitbox = (self.x + 4, self.y + 10, 28, 25)

    def draw(self, win):
        self.move()
        if self.walkCount + 1 >= 15:
            self.walkCount = 0
        if self.vel > 0:
            win.blit(self.walkRight[self.walkCount // 5], (self.x, self.y))
            self.walkCount += 1
        else:
            win.blit(self.walkLeft[self.walkCount // 5], (self.x, self.y))
            self.walkCount += 1
        self.hitbox = (self.x + 4, self.y + 10, 28, 25)
        pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)

    def move(self):
        if self.vel > 0:
            if self.x + self.vel < self.path[1]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkCount = 0
        else:
            if self.x - self.vel > self.path[0]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkCount = 0

    def hit(self):
        print('hit')
        pass

def redrawGameWindow():
    win.blit(bg, (0, 0))
    win.blit(fg, (0, 332))
    win.blit(pilv1, (0, 0))
    win.blit(pilv2, (450, 50))
    fox.draw(win)
    eagle.draw(win)
    for bullet in bullets:
        bullet.draw(win)
    for cloud in clouds:
        cloud.draw(win)

    pygame.display.update()
#MAINLOOP
fox = player(200, 300, 32, 32)
eagle = enemy(50, 300, 32, 32, 750)
bullets = []
clouds = []
run = True
while run:
    clock.tick(60)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
    for cloud in clouds:
        if cloud.x < 800 and cloud.x > 0:
            cloud.x += cloud.vel    
        if len(clouds) < 2:
            clouds.append(pilv1) or clouds.append(pilv2)
        else:
            clouds.pop(clouds.index(cloud))
            
    for bullet in bullets:
        if bullet.y - bullet.radius < eagle.hitbox[1] + eagle.hitbox[3] and bullet.y + bullet.radius > eagle.hitbox[1]:
            if bullet.x + bullet.radius > eagle.hitbox[0] and bullet.x - bullet.radius < eagle.hitbox[0] + eagle.hitbox[2]:
                eagle.hit()
                bullets.pop(bullets.index(bullet))
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
            bullets.append(projectile(round(fox.x + fox.width//2), round(fox.y + fox.height//2), 2, (0, 0, 0), facing))
    if keys[pygame.K_LEFT] and fox.x > fox.vel:
        fox.x -= fox.vel
        fox.left = True
        fox.right = False
        fox.idle = False

    elif keys[pygame.K_RIGHT] and fox.x < screenWidth - 30:
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
