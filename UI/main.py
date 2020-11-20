import pygame, math, time, random, os
# from player.py import Player

# colours

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (130,130,130)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# load map branch
pygame.init()

# sprite variables
map_sprite = pygame.sprite.Group()
player_sprite = pygame.sprite.Group()

# grab the map image from the main manu
# from main_menu import map_img_name
# aa why is not importing the image :(
# put current, resource, and image path into the main menu function 20201119
map_img_name = 'Map_Final.png'

#current_path = os.path.dirname(__file__)
#resource_path = os.path.join(current_path, 'resources')
#image_path = os.path.join(resource_path, 'images')

map_img = pygame.image.load(map_img_name)


# these are to be used for scaling things later

def map_width():
    width = int(map_img.get_rect().size[0])
    return width


def map_height():
    height = int(map_img.get_rect().size[1])
    return height


# window set up
# draw a screen to be the size of the map

screen = pygame.display.set_mode((map_width(), map_height()))

screen.fill(GRAY)
pygame.display.set_caption(os.path.splitext(map_img_name)[0])
icon_img_name = 'skeleton-idle_6.png'
icon_img = pygame.image.load(icon_img_name)
pygame.display.set_icon(icon_img)

pygame.display.flip()



# grab the player image from the main menu
# from main_menu import player_img_name

player_img = 'survivor-idle_knife_0.png'


def player_width():
    width = int( player_img.get_rect().size[0]/(map_width()*2) )
    return width


def player_height():
    height = int( player_img.get_rect().size[1]/(map_height()*2) )
    return height

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(player_img)
        self.rect = pygame.transform.scale(screen, (player_width(), player_height()))


# movement properties
# maybe grab difficulty multiplier here?
player_speed = 1*2 # * difficulty


# initializes the map and its movement

class Map(pygame.sprite.Sprite):
    def __init__(self, img):
        super().__init__()
        self.image = pygame.image.load(img)
        self.rect = self.image.get_rect()
        # self.rect = pygame.transform.scale(screen, (map_width()*4, map_height()*4))

    def update(self):
        # movement
        entitySpeed = [0, 0]
        # if key down
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d:
                entitySpeed[0] = player_speed
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                entitySpeed[0] = -player_speed
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                entitySpeed[1] = -player_speed
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                entitySpeed[1] = player_speed
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

        map_sprite.rect.x = pos[0]
        map_sprite.rect.y = pos[1]

        if self.rect.x <= 0:
            self.rect.x = 0
        elif (self.rect.x + player_width()) >= map_width():
            self.rect.x = map_width() - player_width()
        if self.rect.y <= 0:
            self.rect.y = 0
        elif (self.rect.y + player_height()) >= map_height():
            self.rect.y = map_height() - player_height()

        self.rect.x += entitySpeed[0]
        self.rect.y += entitySpeed[1]

# function for determining player movement speed on a map
# may not be needed if movement is in the map section

def move():
    entitySpeed = [0, 0]
    # if key down
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_d:
            entitySpeed[0] = player_speed
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_a:
            entitySpeed[0] = -player_speed
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_w:
            entitySpeed[1] = -player_speed
    if event.type == pygame.KEYDOWN:
         if event.key == pygame.K_s:
            entitySpeed[1] = player_speed
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


# level init
clock = pygame.time.Clock()

running = True

running = True


# init sprites
map_sprite.add(Map(map_img_name))


# adding sprites

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


        screen.blit(pygame.image.load(player_img), (0, 0))
        player_sprite.draw(screen)

        clock.tick(60)
        player_sprite.update()
        pygame.display.update()



