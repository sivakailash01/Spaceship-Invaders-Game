import pygame
import random
import math
#Background file
from pygame import mixer

# Intializing the pygame
pygame.init()
# Creating a window
screen = pygame.display.set_mode((800, 600))

# Title and Icon
pygame.display.set_caption("Space Invasion")
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

background = pygame.image.load('background.png')

# Background
mixer.music.load("background1.wav")
mixer.music.play(-1)



# Player
playerImage = pygame.image.load('space-invaders.png')
playerX = 370
playerY = 480
playerX_change = 0

# Enemy
enemyImage =[]
enemyX =[]
enemyY =[]
enemyX_change =[]
enemyY_change =[]
num_of_enemies =6

for i in range(num_of_enemies):
        enemyImage.append( pygame.image.load('alien.png'))
        enemyX.append(random.randint(0, 735))
        enemyY.append(random.randint(50, 150))
        enemyX_change.append(4)
        enemyY_change.append(40)

# Bullet
BulletImage = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 4
bulletY_change = 10
bullet_state = "ready"

#score
score_value =0
font = pygame.font.Font('freesansbold.ttf', 32)
textX =10
textY =10


#game over text
over_font =pygame.font.Font('freesansbold.ttf', 64)


def show_score(x,y):
    score =font.render("Score: "+str(score_value), True,(255,200,255))
    screen.blit(score,(x,y))

def game_over_text():
    over_text = over_font.render("Game Over", True, (255, 250, 255))
    screen.blit(over_text, (200, 250))

def iscollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + math.pow(enemyY - bulletY, 2))
    if distance < 27:
        return True
    else:
        return False


def player(X, Y):
    screen.blit(playerImage, (X, Y))


def enemy(X, Y,i):
    screen.blit(enemyImage[i], (X, Y))


def fire_bullet(X, Y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(BulletImage, (X + 16, Y + 10))


    # Game Loop
running = True
while running:
    # RGB -Red, Blue, Green
    screen.fill((0, 0, 0))

    # Background Image

    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Finding whether which key has been pressed
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                playerX_change += 5
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_Sound = mixer.Sound('laser.wav')
                    bullet_Sound.play()
                    bulletX = playerX
                    fire_bullet(playerX, playerY)
                    bulletY -= bulletY_change

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # Checking for boundaries of Spaceship
    # 5 = 5+ -0.3 or +0.3 this is the algorithm used here
    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # Enemy movement
    for i in range(num_of_enemies):

        #Game Over
        if enemyY[i] >440:
            for j in range(num_of_enemies):
                enemyY[j]=2000
                game_over_text()
                break
        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 4
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -4
            enemyY[i] += enemyY_change[i]

        # Collision
        collision = iscollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_Sound =mixer.Sound('explosion.wav')
            explosion_Sound.play()
            bulletY = 400
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 800)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)


    # Bullet Movement
    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"



    player(playerX, playerY)
    show_score(textX,textY)
    pygame.display.update()
