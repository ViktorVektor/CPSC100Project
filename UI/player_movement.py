import pygame
#import main
import time

playerX = 0
playerY = 0
playerName = 0

#from main import playerImg
def a():
    #pygame.screen.fill((255, 255, 255))
    print("help lol")

def initPlayer(startX, startY, speedMultiplier):
    #playerName = pygame.image.load(playerImg)
    playerX = startX
    playerY = startY
    main.screen.blit(playerImg, startX, startY)
    main.display.update()


# playerMoveX
# moves
def playerMove():
    if main.event.type == pygame.KEYDOWN:
        if main.event.key == pygame.K_a:
            playerMoveX('a',1, "left")


def playerMoveX(key, multiplier, direction):
    speed = 1 * multiplier
    if direction == "left":
        speed *= -1
    else:
        speed *= 1
    while key:
        playerMoveX(playerName.rect.move(speed, 0))
        #screen.blit(playerName, (currentX + speed), playerY)
        main.display.update()
