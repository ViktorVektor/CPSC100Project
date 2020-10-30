import pygame
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

playerWidth = int(mapWidth/48)
playerHeight = int(mapHeight/35)

playerImg = pygame.transform.scale(playerImg, (playerWidth, playerHeight))

playerX = int(mapImg.get_rect().size[0]/2) # place at the centre
playerDX = 0

playerY = int(mapImg.get_rect().size[1]/2)
playerDY = 0

playerSpeed = 2

#enemy
enemyImg = pygame.image.load('CPSC_Enemy1.png')

enemyWidth = int(mapImg.get_rect().size[0]/48)
enemyHeight = int(mapImg.get_rect().size[1]/15)

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
    screen.blit(playerImg, (playerX, playerY))

def enemy(xPos, yPos):
    screen.blit(enemyImg, (enemyX, enemyY))

# Main Game Loop
running = True
while running:
    #screen.blit(playerImg, (playerX, playerY))
    map(0,0)
    #screen.fill((0, 128, 0))

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

        # enemt movement
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

    # boundary check
    if playerX <= 0:
        playerX = 0
    elif (playerX + playerWidth) >= mapWidth:
        playerX = mapWidth - playerWidth
    if playerY <= 0:
        playerY = 0
    elif (playerY + playerHeight) >= mapHeight:
        playerY = mapHeight - playerHeight

    # collision detection with enemy
    # if the distance between the two objects is zero, then they have collided
    # boundaries: between enemy and player, distance between is (player)


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