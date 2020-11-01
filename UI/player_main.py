import pygame
import math

# playerX, playerY, speed
position = [0, 0]
entityName = ""
entityX = 0
entityY = 0
eS = 2


# entityDX, entityDY, entitySpeed
def entity_init(entity, eX, eY, speed):
    position[0] = eX
    position[1] = eY
    eS = speed


def move(eventGet):

    # if key down
    if (eventGet.type == pygame.KEYDOWN):
        if eventGet.key == pygame.K_d:
            position[0] += eS
            print("Right")
        if eventGet.key == pygame.K_a:
            position[0] += -eS
            print("Left")
        if eventGet.key == pygame.K_w:
            position[1] += -eS
            print("Up")
        if eventGet.key == pygame.K_s:
            position[1] += eS
            print("Down")


    #position[0] = eX + speed
    #position[1] = eY + speed
    print(position[0])
    print(position[1])