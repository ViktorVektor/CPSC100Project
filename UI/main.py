import pygame
import time

# Must initialize pygame upon starting a game
pygame.init()

# draw screen, width height
screen = pygame.display.set_mode((800,600))

# Title
pygame.display.set_caption("meinkraft")

# Icon
icon = pygame.image.load('lorghead.png')
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load('lorghead.png')
playerX = 400
playerY = 300

def playerInit():
    #player_movement.initPlayer(playerX, playerY, 1)
    from player_movement import a
    a()

# Main Game Loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # Pressing the windows close button
            running = False
    # hex rgb
    # should respect order of operation for layers (draw characters on top)
    screen.fill((0,128,0))
    playerInit()
    pygame.display.update()

    #for x in range(0, 255):
    #   screen.fill((x, x, x))
    #    pygame.display.update() # update the display whilet he run loop is running
    #    time.sleep(0.01)
    #for x in range(0, 255):
    #    screen.fill((255-x, 255-x, 255-x))
    #    pygame.display.update() # update the display whilet he run loop is running
    #    time.sleep(0.01)