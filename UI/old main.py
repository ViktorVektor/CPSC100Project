import pygame
import math
#from mobMovement.mob_movement_main import Mob

import time

#from player_main import entity_init, move, position


# Must initialize pygame upon starting a game
pygame.init()

# map
#mapImg = pygame.image.load('CPSC_Map_TundraRough.png')
mapImg = pygame.image.load('Map_Final.png')

def mapWidth():
    mapWidth = int(mapImg.get_rect().size[0])
    return mapWidth

def mapHeight():
    mapHeight = int(mapImg.get_rect().size[1])
    return mapHeight

#screen = pygame.display.set_mode((800,400))
screen = pygame.display.set_mode(mapImg.get_rect().size, 0, 32)

# Title
pygame.display.set_caption("meinkraft")

# Icon
iconImg = 'lorghead.png'
icon = pygame.image.load('lorghead.png')
pygame.display.set_icon(icon)



# Player

playerImg = icon

player_width() = int(mapWidth()/43)*5
playerHeight = int(mapHeight()/35)*5

playerImg = pygame.transform.scale(playerImg, (player_width(), playerHeight))

# spawn point
playerX = int(mapImg.get_rect().size[0]/2) # place at the centre
playerDX = 0

playerY = int(mapImg.get_rect().size[1]/2)
playerDY = 0

playerSpeed = 2

WHITE = (255, 255, 255)

def move():
    entitySpeed = [0, 0]
    # if key down
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_d:
            entitySpeed[0] = playerSpeed
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_a:
            entitySpeed[0] = -playerSpeed
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_w:
            entitySpeed[1] = -playerSpeed
    if event.type == pygame.KEYDOWN:
         if event.key == pygame.K_s:
            entitySpeed[1] = playerSpeed
    # if key upsd
    if event.type == pygame.KEYUP:
         if event.key == pygame.K_d:
            entitySpeed[0] = 0
    if event.type == pygame.KEYUP:
         if event.key == pygame.K_a:
            entitySpeed[0] = 0
    if event.type == pygame.KEYUP:
        if event.key == pygame.K_w:
            entitySpeed[1] = 0
    if event.type == pygame.KEYUP:
        if event.key == pygame.K_s:
            entitySpeed[1] = 0

    return entitySpeed

class sprites(pygame.sprite.Sprite):
    def __init__(self, img, playerX, playerY):
        super().__init__()

        self.image = pygame.Surface((playerX, playerY))
        self.image.fill(WHITE)

        self.rect = self.image.get_rect()

    def update(self):
        self.rect.x = 400
        self.rect.y = 400


class Player(pygame.sprite.Sprite):
    def __init__(self, img, player_width, playerHeight):
        super().__init__()
        self.image = pygame.image.load(img)
        self.size = pygame.transform.scale(self.image, (player_width(), playerHeight))

        self.rect = self.image.get_rect()

    def update(self):
        # movement
        entitySpeed = [0, 0]
        # if key down
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d:
                entitySpeed[0] = playerSpeed
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                entitySpeed[0] = -playerSpeed
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                entitySpeed[1] = -playerSpeed
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                entitySpeed[1] = playerSpeed
        # if key upsd
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_d:
                entitySpeed[0] = 0
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                entitySpeed[0] = 0
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                entitySpeed[1] = 0
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_s:
                entitySpeed[1] = 0

        pos = pygame.mouse.get_pos()

        playerSprite.rect.x = pos[0]
        playerSprite.rect.y = pos[1]

        if self.rect.x <= 0:
            self.rect.x = 0
        elif (self.rect.x + player_width()) >= mapWidth():
            self.rect.x = mapWidth() - player_width()
        if self.rect.y <= 0:
            self.rect.y = 0
        elif (self.rect.y + playerHeight) >= mapHeight():
            self.rect.y = mapHeight() - playerHeight

        self.rect.x += entitySpeed[0]
        self.rect.y += entitySpeed[1]



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


#def player(xPos, yPos):
 #   screen.blit(playerImg, (xPos, yPos))


def enemy(xPos, yPos):
    screen.blit(enemyImg, (xPos, yPos))


# sprite positions are considered to be the top left corner of the sprite
# between two touching entities, it's either they top-bottom or left-right touching, never top-top or right-right
# returns an array of {a_Top-b_Bottom, a_Bottom-b_Top, a_Left-b_Right, a_Right-b_bottom} distances

# Main Game Loop
running = True

position = [0, 0]
entityName = ""
eS = 2


# entityDX, entityDY, entitySpeed
def entity_init(entity, eX, eY, speed):
    position[0] = eX
    position[1] = eY
    eS = speed

#groups
enemies = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
player = pygame.sprite.Group()


normalSprite = sprites(WHITE, 500, 400)
playerSprite = Player("lorghead.png", player_width(), playerHeight)

all_sprites.add(normalSprite)
player.add(playerSprite)

clock = pygame.time.Clock()

while running:
    # screen.blit(playerImg, (playerX, playerY))
    map(0, 0)
    # screen.fill((0, 128, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # Pressing the windows close button
            running = False





        position[0] = playerX
        position[1] = playerY

        #sprite collision check
        #all_sprites = pygame.sprite.spritecollide(player, all_sprites, True)

        all_sprites.draw(screen)
        player.draw(screen)
        clock.tick(60)

        all_sprites.update()
        player.update()
        sprites.update(normalSprite)
        pygame.display.update()
        #movePlayer(event)
        #if key down
        #if event.type == pygame.KEYDOWN:
        #    if event.key == pygame.K_d:
        #        playerDX = playerSpeed
        #if event.type == pygame.KEYDOWN:
        ##    if event.key == pygame.K_a:
         #      playerDX = -playerSpeed
        #if event.type == pygame.KEYDOWN:
        #    if event.key == pygame.K_w:
        ##       playerDY = -playerSpeed
        #if event.type == pygame.KEYDOWN:
            #if event.key == pygame.K_s:
             #   playerDY = playerSpeed
        # if key upsd
        #if event.type == pygame.KEYUP:
           # if event.key == pygame.K_d:
          #     playerDX = 0
        #if event.type == pygame.KEYUP:
          # if event.key == pygame.K_a:
         #       playerDX = 0
        #if event.type == pygame.KEYUP:
        #   if event.key == pygame.K_w:
         #      playerDY = 0
        #if event.type == pygame.KEYUP:
        #    if event.key == pygame.K_s:
        #        playerDY = 0

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

    #playerX += playerDX
    #playerY += playerDY

    # collision detection with enemy
    # if the distance between the two objects is zero, then they have collided
    # upon distance = 0, dx or dy = 0




    enemyX += enemyDX
    enemyY += enemyDY
    #player(playerX, playerY)
    enemy(enemyX, enemyY)


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