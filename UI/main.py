import pygame
import time

# Must initialize pygame upon starting a game
pygame.init()

# map
mapImg = pygame.image.load('CPSC_Map_TundraRough.png')

#screen = pygame.display.set_mode((800,400))
screen = pygame.display.set_mode(mapImg.get_rect().size, 0, 32)

# Title
pygame.display.set_caption("meinkraft")

# Icon
icon = pygame.image.load('lorghead.png')
pygame.display.set_icon(icon)



# Player
playerImg = pygame.image.load('CPSC_Enemy1.png')

playerWidth = int(mapImg.get_rect().size[0]/48)
playerHeight = int(mapImg.get_rect().size[1]/15)

playerImg = pygame.transform.scale(playerImg, (playerWidth, playerHeight))

playerX = 400
playerDX = 0

playerY = 300
playerDY = 0

playerSpeed = 2

# draw screen, width height


def map(xPos, yPos):
    screen.blit(mapImg, (xPos,yPos))

def player(xPos, yPos):
    screen.blit(playerImg, (playerX, playerY))

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

    playerX += playerDX
    playerY += playerDY
    player(playerX, playerY)
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