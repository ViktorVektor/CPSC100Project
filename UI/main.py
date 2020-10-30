import pygame
import math

import time

# Must initialize pygame upon starting a game
pygame.init()

# map
#mapImg = pygame.image.load('CPSC_Map_TundraRough.png')
mapImg = pygame.image.load('Map_Final.png')

mapWidth = int(mapImg.get_rect().size[0])
mapHeight = int(mapImg.get_rect().size[1])

#screen = pygame.display.set_mode((800,400))
screen = pygame.display.set_mode(mapImg.get_rect().size, 0, 32)

# Title
pygame.display.set_caption("meinkraft")

# Icon
icon = pygame.image.load('lorghead.png')
pygame.display.set_icon(icon)



# Player
playerImg = icon

playerWidth = int(mapWidth/43)*5
playerHeight = int(mapHeight/35)*5

playerImg = pygame.transform.scale(playerImg, (playerWidth, playerHeight))

playerX = int(mapImg.get_rect().size[0]/2) # place at the centre
playerDX = 0

playerY = int(mapImg.get_rect().size[1]/2)
playerDY = 0

playerSpeed = 2

#enemy
enemyImg = pygame.image.load('CPSC_Enemy1.png')

enemyWidth = int(mapImg.get_rect().size[0]/48)*5
enemyHeight = int(mapImg.get_rect().size[1]/15)*5

enemyImg = pygame.transform.scale(enemyImg, (enemyWidth, enemyHeight))

enemyX = int(mapImg.get_rect().size[0]/2)
enemyDX = 0

enemyY = int(mapImg.get_rect().size[0]/2)
enemyDY = 0

enemySpeed = 1
# draw screen, width height


def map(xPos, yPos):
    screen.blit(mapImg, (xPos,yPos))


def player(xPos, yPos):
    screen.blit(playerImg, (xPos, yPos))


def enemy(xPos, yPos):
    screen.blit(enemyImg, (xPos, yPos))


# sprite positions are considered to be the top left corner of the sprite
# between two touching entities, it's either they top-bottom or left-right touching, never top-top or right-right
# returns an array of {a_Top-b_Bottom, a_Bottom-b_Top, a_Left-b_Right, a_Right-b_bottom} distances
def distance(aX, aY, aWidth, aHeight, bX, bY, bWidth, bHeight):

    boundary_distance = [0, 0, 0, 0]

    a_top = aY
    a_bottom = aY + int(aHeight)
    a_left = aX
    a_right = aX + int(aWidth)

    b_top = bY
    b_bottom = bY + int(bHeight)
    b_left = bX
    b_right = bX + int(bWidth)

    boundary_distance[0] = math.fabs(a_top - b_bottom)
    boundary_distance[1] = math.fabs(a_bottom - b_top)
    boundary_distance[2] = math.fabs(a_left - b_right)
    boundary_distance[3] = math.fabs(a_right - b_left)

    return boundary_distance


# Main Game Loop
running = True
while running:
    # screen.blit(playerImg, (playerX, playerY))
    map(0, 0)
    # screen.fill((0, 128, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # Pressing the windows close button
            running = False

        # if key down
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d:
                playerDX = playerSpeed
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                playerDX = -playerSpeed
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                playerDY = -playerSpeed
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                playerDY = playerSpeed
        # if key up
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_d:
                playerDX = 0
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                playerDX = 0
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                playerDY = 0
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_s:
                playerDY = 0

        # enemy movement
        # if key down
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                enemyDX = playerSpeed
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                enemyDX = -playerSpeed
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                enemyDY = -playerSpeed
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                enemyDY = playerSpeed
        # if key up
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                enemyDX = 0
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                enemyDX = 0
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                enemyDY = 0
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                enemyDY = 0

    playerX += playerDX
    playerY += playerDY

    # collision detection with enemy
    # if the distance between the two objects is zero, then they have collided
    # upon distance = 0, dx or dy = 0


    top_bottom_distance = \
        distance(playerX, playerY, playerWidth, playerHeight, enemyX, enemyY, enemyWidth, enemyHeight)[0]
    bottom_top_distance = \
        distance(playerX, playerY, playerWidth, playerHeight, enemyX, enemyY, enemyWidth, enemyHeight)[1]
    left_right_distance = \
        distance(playerX, playerY, playerWidth, playerHeight, enemyX, enemyY, enemyWidth, enemyHeight)[2]
    right_left_distance = \
        distance(playerX, playerY, playerWidth, playerHeight, enemyX, enemyY, enemyWidth, enemyHeight)[3]

    # if player top and enemy bottom are touching
    # needs the extra left and right side conditions so it only stops within the width of the enemy
    # THINGS KEEP CLIPPING AND I DON'T KNOW WHY AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA 2020 10 30
    if (top_bottom_distance <= 2) \
            and (left_right_distance - enemyWidth <= enemyWidth + 12) \
            and (right_left_distance - enemyWidth <= enemyWidth + 12):
        playerY -= playerDY
        enemyY -= enemyDY
    # if player bottom and enemy top
    if (bottom_top_distance <= 2) \
            and (left_right_distance - enemyWidth <= enemyWidth + 12) \
            and (right_left_distance - enemyWidth <= enemyWidth + 12):
        playerY -= playerDY
        enemyY -= enemyDY
    # if player left and enemy right
    if(left_right_distance <= 2) \
            and (top_bottom_distance - enemyHeight <= enemyWidth) \
            and (bottom_top_distance - enemyHeight <= enemyWidth):
        playerX -= playerDX
        enemyX -= enemyDX
    # if player right and enemy left
    if(right_left_distance <= 2) \
            and (top_bottom_distance - enemyHeight <= enemyWidth)\
            and (bottom_top_distance - enemyHeight <= enemyWidth):
        playerX -= playerDX
        enemyX -= enemyDX

    # boundary check
    if playerX <= 0:
        playerX = 0
    elif (playerX + playerWidth) >= mapWidth:
        playerX = mapWidth - playerWidth
    if playerY <= 0:
        playerY = 0
    elif (playerY + playerHeight) >= mapHeight:
        playerY = mapHeight - playerHeight

    enemyX += enemyDX
    enemyY += enemyDY
    player(playerX, playerY)
    enemy(enemyX, enemyY)

    pygame.display.update()

    #for x in range(0, 255):
    #    screen.fill((x, x, x))
    #    player()
    #    pygame.display.update() # update the display whilet he run loop is running
    #    time.sleep(0.01)
    #for x in range(0, 255):
    #    screen.fill((255-x, 255-x, 255-x))
    #    player()
    #    pygame.display.update() # update the display whilet he run loop is running
    #    time.sleep(0.01)