# Agenda: moving the enemy   <<<<<<<<<< ====================

import math

import pygame
import random
from pygame import mixer

# Intialize the pygame
pygame.init()

# create the screen
screen = pygame.display.set_mode((800, 600))

#background
background=pygame.image.load('background.png')
background=background.convert_alpha()

# Title (aka Caption) and Icon
pygame.display.set_caption("Space Invader")
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

# Score   <<<<<<<<<< ====================
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

# Where to display the score?  <<<<<<<<<< ====================
textX = 10
testY = 10


# Show score   <<<<<<<<<< ====================
def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))
#game over 
over_font=pygame.font.Font('freesansbold.ttf',64)
def game_over_text():
    over_text=over_font.render("GAME OVER",True,(255,255,255))
    screen.blit(over_text,(200,250))
# Player
playerImg = pygame.image.load('player.png')
playerX = 370
playerY = 480
playerX_change = 0

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(1)
    enemyY_change.append(40)

#bullet
bulletimg=pygame.image.load('bullet.png')
bulletImg=bulletimg.convert_alpha()
bulletx=0
bullety=480
bulletx_change=0
bullety_change=1
bullet_state="ready"

def player(x, y):
    screen.blit(playerImg, (x, y))

# Enemy
def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))
#bullet
def fire_bullet(x,y):
    global bullet_state
    bullet_state="fire"
    screen.blit(bulletImg,(x+16,y+10))
#collusion
def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False

# Game Loop
running = True
while running:

    # RGB = Red, Green, Blue
    screen.fill((0, 0, 0))
    screen.blit(background,(0,0))

    # Capture and check events one by one
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -1
            if event.key == pygame.K_RIGHT:
                playerX_change = 1
            if event.key==pygame.K_SPACE:
                if bullet_state=="ready":
                    bulletx=playerX
                    fire_bullet(playerX,bullety)
                    bulletsound=mixer.Sound("laser.wav")
                    bulletsound.play()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # Change position of the player
    playerX += playerX_change

    # Adding boundaries to our game
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:  # 800px - 64px (64px is width of pic)
        playerX = 736

    # Change position of the enemy   <<<<<<<<<< ====================
    for i in range(num_of_enemies):
        if enemyY[i]>440:
            for j in range(num_of_enemies):
                enemyY[j]=2000
            game_over_text()
            break
        enemyX[i] += enemyX_change[i]

        # Enemy movement. if hits right, go left and vice-versa   <<<<<<<<<< ====================

        if enemyX[i] <= 0:
            enemyX_change[i] = 0.3
            enemyY[i] += enemyY_change[i]

        elif enemyX[i] >= 736:  # 800px - 64px (64px is width of pic)
            enemyX_change[i] = -0.3
            enemyY[i] += enemyY_change[i]
        #bullet
        if bullet_state is "fire":
            fire_bullet(bulletx,bullety)
            bullety-=bullety_change
        if bullety<0:
            bullety=480
            bullet_state="ready"
        #collusion
        collision = isCollision(enemyX[i], enemyY[i], bulletx, bullety)
        if collision:
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            print(score_value)
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(50, 150)
            crashsound=mixer.Sound("explosion.wav")
            crashsound.play()
        # Draw the player
        player(playerX, playerY)

        # Draw the enemy
        enemy(enemyX[i],enemyY[i],i)
    show_score(textX,testY)
    # update the screen
    pygame.display.update()