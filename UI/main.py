import pygame, math, time, random, os
# from player.py import Player

# colours

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (130,130,130)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# settings
REFRESH_RATE = 60
MAP_ZOOM = 2
FONT = 32
# movement properties
# maybe grab difficulty multiplier here?
PLAYER_SPEED = 1 * 3 # * difficulty

# load map branch
pygame.init()

# sprite variables
map_sprite = pygame.sprite.Group()
player_sprite = pygame.sprite.Group()
barrier_sprites = pygame.sprite.Group()

# grab the map image from the main manu
# from main_menu import map_img_name
# aa why is not importing the image :(
# put current, resource, and image path into the main menu function 20201119
map_img_name = 'Map_Final.png'

# grab the player image from the main menu
# from main_menu import player_img_name

player_img_name = 'survivor-idle_knife_0.png'

# barrier sprites
# container_1
container_1_ratio = (2, 4)
container_1 = 'container_1.png'

# current_path = os.path.dirname(__file__)
# resource_path = os.path.join(current_path, 'resources')
# image_path = os.path.join(resource_path, 'images')

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

# uses the name of the map_img_name without the file extension
pygame.display.set_caption(os.path.splitext(map_img_name)[0])

# loads the enemy as the icon
icon_img_name = 'skeleton-idle_6.png'
icon_img = pygame.image.load(icon_img_name)
pygame.display.set_icon(icon_img)

# window  update
pygame.display.flip()

# WASD inputs
KEYS = {pygame.K_w : (0, 1),
        pygame.K_a : (1, 0),
        pygame.K_s : (0, -1),
        pygame.K_d : (-1, 0)}


class Player(pygame.sprite.Sprite):
    def __init__(self, img_name):
        super().__init__()
        # variables for the class
        self.image = pygame.image.load(img_name)
        self.rect = self.image.get_rect()
        self.image = pygame.transform.scale(self.image, (int(map_width() / (MAP_ZOOM * 4)), int(map_height() / (MAP_ZOOM * 4))))
        self.is_north = False
        self.is_east = True
        self.is_west = False
        self.is_south = False

    # face cardinally according to which WASD key is pressed
    def key_face(self):
        if event.type == pygame.KEYDOWN:
            # face up
            if event.key == pygame.K_w:
                if self.is_north:
                    self.image = pygame.transform.rotate(self.image, 0)
                if self.is_south:
                    self.image = pygame.transform.rotate(self.image, 180)
                if self.is_east:
                    self.image = pygame.transform.rotate(self.image, 90)
                if self.is_west:
                    self.image = pygame.transform.rotate(self.image, -90)

                self.is_north = True
                self.is_east = False
                self.is_west = False
                self.is_south = False


            #face down
            if event.key == pygame.K_s:
                if self.is_north:
                    self.image = pygame.transform.rotate(self.image, 180)
                if self.is_south:
                    self.image = pygame.transform.rotate(self.image, 0)
                if self.is_east:
                    self.image = pygame.transform.rotate(self.image, -90)
                if self.is_west:
                    self.image = pygame.transform.rotate(self.image, 90)

                self.is_north = False
                self.is_east = False
                self.is_west = False
                self.is_south = True

            # face left
            if event.key == pygame.K_a:
                if self.is_north:
                    self.image = pygame.transform.rotate(self.image, 90)
                if self.is_south:
                    self.image = pygame.transform.rotate(self.image, -90)
                if self.is_east:
                    self.image = pygame.transform.rotate(self.image, 180)
                if self.is_west:
                    self.image = pygame.transform.rotate(self.image, 0)

                self.is_north = False
                self.is_east = False
                self.is_west = True
                self.is_south = False

            # face right
            if event.key == pygame.K_d:
                if self.is_north:
                    self.image = pygame.transform.rotate(self.image, -90)
                if self.is_south:
                    self.image = pygame.transform.rotate(self.image, 90)
                if self.is_east:
                    self.image = pygame.transform.rotate(self.image, 0)
                if self.is_west:
                    self.image = pygame.transform.rotate(self.image, 180)

                self.is_north = False
                self.is_east = True
                self.is_west = False
                self.is_south = False

    # calculate position of mouse, and turn the character towards it
    def mouse_face(self):
        # for mouse_face
        mouse_x, mouse_y = pygame.mouse.get_pos()
        rel_x, rel_y = mouse_x - self.rect.x, mouse_y - self.rect.y
        angle = (180 / math.pi) * -math.atan2(rel_y, rel_x)

        self.image = pygame.transform.rotate(self.image, int(angle))
        # an attempt to keep the character in the middle of the screen
        # self.rect = self.image.get_rect(center=self.rect.center)

    def player_width(self):
        width = int(self.image.get_rect().size[0] / (map_width() * 2))
        return width

    def player_height(self):
        height = int(self.image.get_rect().size[1] / (map_height() * 2))
        return height

    def update(self):
        # pos = pygame.mouse.get_pos()

        # place the character at the center of the screen
        self.rect.x = int(map_width()/2) - int(self.player_width()/2)
        self.rect.y = int(map_height()/2) - int(self.player_height()/2)

        self.key_face()

        # trying to fix this function, maybe do later if time permits
        # self.mouse_face()


# Class for any barrier elements, (walls, boxes, containers, etc)
# takes the barrier image,tuple position on the map, and the current position of the map.
class Barrier(pygame.sprite.Sprite):
    def __init__(self, img_name, current_pos, place_xy, ratio_xy):
        super().__init__()
        self.image = pygame.image.load(img_name)
        self.image = pygame.transform.scale(self.image, (int(map_width() / (MAP_ZOOM * ratio_xy[0])), int(map_height() / (MAP_ZOOM * ratio_xy[1]))))
        self.speed = PLAYER_SPEED

        self.rect = self.image.get_rect()
        self.current_pos = current_pos
        # initial placement at the start of the level
        self.rect.x = current_pos[0] + place_xy[0] * MAP_ZOOM - self.rect.size[0]
        self.rect.y = current_pos[0] + place_xy[1] * MAP_ZOOM - self.rect.size[1]

    def move(self, keys):
        # movement

        # if the key being pressed is in the array of KEYS
        for key in KEYS:
            if keys[key]:
                # take the value of the tuple and add it do the position
                self.rect.x += KEYS[key][0] * self.speed
                self.rect.y += KEYS[key][1] * self.speed
            pygame.display.flip()

    def update(self, keys):
        # refreshed placement as the player moves
        # self.rect.x = self.current_pos[0] + self.rect.x
        # self.rect.y = self.current_pos[1] +d self.rect.y
        self.move(keys)


# initializes the map and its movement
class Map(pygame.sprite.Sprite):
    def __init__(self, img):
        super().__init__()
        self.image = pygame.image.load(img)
        self.rect = self.image.get_rect()
        self.speed = PLAYER_SPEED
        # self.keys = pygame.key.get_pressed()

    def current_pos(self):
        current_pos = (self.rect.x, self.rect.y)
        return current_pos

    def move(self, keys):
        # movement

        # if the key being pressed is in the array of KEYS
        for key in KEYS:
            if keys[key]:
                # take the value of the tuple and add it do the position
                self.rect.x += KEYS[key][0] * self.speed
                self.rect.y += KEYS[key][1] * self.speed
            pygame.display.flip()

    # self.rect.clamp_ip(map_img.get_rect())  # Keep player on screen.

    def update(self, keys):
        self.image = pygame.transform.scale(map_img, (map_width() * MAP_ZOOM, map_height() * MAP_ZOOM))
        self.move(keys)


# level init
clock = pygame.time.Clock()

running = True

# init sprites
map_one = Map(map_img_name)
map_current_pos = map_one.current_pos()
player_one = Player(player_img_name)

#

# init barrier list
b_one = [None] * 256

b_one[0] = Barrier(container_1, map_current_pos, (502, 180), container_1_ratio)

# add sprites
map_sprite.add(map_one)
player_sprite.add(player_one)

for x in b_one:
    if x != None:
        barrier_sprites.add(x)


# game loop

# built in font and font size
# can turn off these readouts afterwards
font = pygame.font.Font('freesansbold.ttf', 16)

text_resolution = font.render('width: ' + str(map_width()) + ' eight: ' + str(map_height()), True, GREEN, BLACK)
text_refresh= font.render('refresh rate: ' + str(REFRESH_RATE), True, GREEN, BLACK)
text_map_zoom = font.render('map zoom: ' + str(MAP_ZOOM), True, GREEN, BLACK)
text_player_speed = font.render('player speed: ' + str(PLAYER_SPEED), True, GREEN, BLACK)

# drawing text rect for positioning
text_rect_1 = text_resolution.get_rect()
text_rect_2 = text_refresh.get_rect()
text_rect_3 = text_map_zoom.get_rect()
text_rect_4 = text_player_speed.get_rect()

while running:
    # draw sprites
    map_sprite.draw(screen)
    player_sprite.draw(screen)
    barrier_sprites.draw(screen)

    key_pressed = pygame.key.get_pressed()

    # where the actual movement is, should be outside of the event loop
    map_sprite.update(key_pressed)
    barrier_sprites.update(key_pressed)

    screen.blit(text_resolution, text_rect_1)
    screen.blit(text_refresh, (text_rect_2.x, text_rect_2.y + 16))
    screen.blit(text_map_zoom, (text_rect_3.x, text_rect_3.y + 32))
    screen.blit(text_player_speed, (text_rect_4.x, text_rect_4.y + 48))

    pygame.display.update()
    # event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # screen.blit(pygame.image.load(player_img_name), (0, 0))

        clock.tick(REFRESH_RATE)

        player_sprite.update()





