import pygame
import time

playerX = 0
playerY = 0
playerName = 0


def initPlayer(playerImg, startX, startY, speedMultiplier):
    playerName = pygame.image.load(playerImg)
    playerX = startX
    playerY = startY

    screen.blit(playerImg, startX, startY)
    pygame.display.update()


# playerMoveX
# moves
def playerMove():
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_a:
            playerMoveX('a',1, left)


def playerMoveX(key, multiplier, direction):
    speed = 1 * multiplier
    if direction == "left":
        speed *= -1
    else:
        speed *= 1
    while key:
        playerMoveX(playerName.rect.move(speed, 0))
        #screen.blit(playerName, (currentX + speed), playerY)
        pygame.display.update()
