# Group: 82
# Course: CPSC 100
# Lab: L1M
# Date: 2020 Nov 23
# Authors:
#       Elijah Cuico
#       Viktor Moreno 75388181
#
# Title: Sneaky Beaky (the game)
# Description:
# A mini game where you sneak around to try and avoid enemies who are searching for you. Enemies will try to guess
# where the player will go through position, amount of movement, and some algorithms to determine likely positions.

import pygame, math, time, random, os
# from player.py import Player

# colours

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (130,130,130)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Directions
NORTH = 0
SOUTH = 1
EAST = 2
WEST = 3

# settings
REFRESH_RATE = 60
MAP_ZOOM = 2
FONT = 32
# movement properties
# maybe grab difficulty multiplier here?
PLAYER_SPEED = 1 * 3 # * difficulty

# load map branch
pygame.init()

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
container_ratio = (1.9, 3.8)
container_1 = 'container_1.png'

container_2 = 'container_2.png'

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
KEYS = {pygame.K_w: (0, 1),
        pygame.K_a: (1, 0),
        pygame.K_s: (0, -1),
        pygame.K_d: (-1, 0)}


# class for player
# takes player img filename
class Player(pygame.sprite.Sprite):
    def __init__(self, img_name):
        super().__init__()
        self.image = pygame.image.load(img_name)
        self.rect = self.image.get_rect()
        self.image = pygame.transform.scale(self.image, (int(map_width() / (MAP_ZOOM * 4)), int(map_height() / (MAP_ZOOM * 4))))
        self.rect.width = (int(map_width() / (MAP_ZOOM * 5)))
        self.rect.height = (int(map_height() / (MAP_ZOOM * 4)))
        # place the character at the center of the screen
        self.rect.x = int(map_width() / 2) - int(self.player_width() / 2)
        self.rect.y = int(map_height() / 2) - int(self.player_height() / 2)

        # for direction facing
        self.is_north = False
        self.is_east = True
        self.is_west = False
        self.is_south = False

    # returns a number 0 1 2 3 for north south east west
    def facing(self):
        output = 0
        if self.is_north:
            output = NORTH
        if self.is_south:
            output = SOUTH
        if self.is_east:
            output = EAST
        if self.is_west:
            output = WEST
        return output

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
        pygame.draw.rect(screen, GREEN, (self.rect.x, self.rect.y, self.rect.width, self.rect.height), 0)
        # trying to fix this function, maybe do later if time permits
        # self.mouse_face()


# Class for any barrier elements, (walls, boxes, containers, etc)
# takes the barrier image,tuple position on the map, and the current position of the map.
class Barrier(pygame.sprite.Sprite):
    def __init__(self, img_name, current_pos, place_xy, ratio_xy):
        super().__init__()

        self.image = pygame.image.load(img_name)
        self.rect = self.image.get_rect()
        self.rect = self.rect

        self.image = pygame.transform.scale(self.image,
                                            (int(map_width() / (MAP_ZOOM * ratio_xy[0])),
                                             int(map_height() / (MAP_ZOOM * ratio_xy[1]))))
        self.rect.width = (int(map_width() / (MAP_ZOOM * ratio_xy[0])))
        self.rect.height = (int(map_height() / (MAP_ZOOM * ratio_xy[1])))

        self.speed = PLAYER_SPEED

        self.current_pos = current_pos
        # initial placement at the start of the level
        self.rect.left = map_current_pos[0] + place_xy[0] * MAP_ZOOM - self.rect.size[0]
        self.rect.top = map_current_pos[0] + place_xy[1] * MAP_ZOOM - self.rect.size[1]

        # for barrier collisions
        self.players = player_sprite

        self.collision = False

    # for outside reference
    def has_collided(self):
        return self.collision

    def move(self, keys):
        # movement and collision

        no_keys = {pygame.K_w: (0, 0),
                    pygame.K_a: (0, 0),
                    pygame.K_s: (0, 0),
                    pygame.K_d: (0, 0)}

        # if the key being pressed is in the array of KEYS
        dx = 0
        dy = 0

        for x in KEYS:
            if keys[x]:
                dx += (KEYS[x][0] * self.speed)
                dy += (KEYS[x][1] * self.speed)

        player_collisions = pygame.sprite.groupcollide(barrier_sprites, self.players, False, False)

        for players in player_collisions:
            # if the player top goes into the barrier bottom with a 3 pixel padding
            if players.rect.top < (self.rect.bottom + 3) and players.rect.bottom < (self.rect.top - 3):
                self.collision = True
                self.rect.y -= 3

                if players.rect.bottom > (self.rect.top - 3):
                    self.collision = True
                    self.rect.y += 3
                else:
                    self.rect.y += 3
            else:
                self.rect.y -= 3


        for maps in map_sprite:
            if maps.has_collided():
                dx = 0
                dy = 0

        self.rect.x += dx
        self.rect.y += dy


    def update(self, keys):
        # refreshed placement as the player moves
        #self.rect.x = self.current_pos[0] + self.rect.x
        #self.rect.y = self.current_pos[1] + self.rect.y
        pygame.draw.rect(screen, RED, (self.rect.x, self.rect.y, self.rect.width, self.rect.height), 0)
        self.collision = False
        self.move(keys)



# initializes the map and its movement
class Map(pygame.sprite.Sprite):
    def __init__(self, img):
        super().__init__()
        self.image = pygame.image.load(img)
        self.image = pygame.transform.scale(self.image, (int(map_width() * MAP_ZOOM), int(map_height() * MAP_ZOOM)))
        self.rect = self.image.get_rect()
        self.rect.width = int(map_width() * MAP_ZOOM + 150)
        self.rect.height = int(map_height() * MAP_ZOOM + 75)

        self.speed = PLAYER_SPEED

        # for barrier collisions from player
        # self.barriers = player_sprite

        self.collision = False

    def current_pos(self):
        current_pos = (self.rect.x, self.rect.y)
        return current_pos

    def has_collided(self):
        return self.collision

    def move(self, keys):
        # movement
        dx = 0
        dy = 0

        Players = player_sprite

        for x in KEYS:
            if keys[x]:
                dx += (KEYS[x][0] * self.speed)
                dy += (KEYS[x][1] * self.speed)

            for player in Players:
                if player.rect.top < self.rect.top:
                    self.collision = True
                    self.rect.top = player.rect.top
                if player.rect.bottom > self.rect.bottom:
                    self.collision = True
                    self.rect.bottom = player.rect.bottom
                if player.rect.left < self.rect.left:
                    self.collision = True
                    self.rect.left = player.rect.left
                if player.rect.right > self.rect.right:
                    self.collision = True
                    self.rect.right = player.rect.right
        for barriers in barrier_sprites:
            if barriers.has_collided():
                dx = 0
                dy = 0

        self.rect.x += dx
        self.rect.y += dy

        # weird movement stop solution but I don't have time :/

        # if the key being pressed is in the array of KEYS
        #for key in KEYS:
        #    if keys[key]:
        #        self.rect.y += KEYS[key][1] * self.speed

        #for x in player_collisions:

            # right of character colliding with bottom of barrier, stop the movement of the map underneath
            # by subtracting the corresponding key direction
        #    if player_one.barrier_top() or player_one.barrier_bottom():
        #        if keys[key]:
        #            self.rect.y = self.temp_y

        #for key in KEYS:
        #    if keys[key]:
        #        self.rect.x += KEYS[key][0] * self.speed

        #for x in player_collisions:
        #    # left or right of character colliding with bottom of barrier, stop the movement of the map underneath
        #    # by subtracting the corresponding key direction
        #    if player_one.barrier_left() or player_one.barrier_right():
        #        if keys[key]:
        #            self.rect.x = self.temp_x

    # self.rect.clamp_ip(map_img.get_rect())  # Keep player on screen.

    def update(self, keys):
        self.collision = False
        self.move(keys)
        #self.temp_x = self.rect.x
        #self.temp_y = self.rect.y


# level init
clock = pygame.time.Clock()

running = True

# sprite variables
map_sprite = pygame.sprite.Group()
player_sprite = pygame.sprite.Group()
barrier_sprites = pygame.sprite.Group()

# giving class Player the list of barriers to use in collision check
player_sprite.barriers = barrier_sprites

# init sprites
map_one = Map(map_img_name)
map_current_pos = map_one.current_pos()
player_one = Player(player_img_name)

# add sprites
map_sprite.add(map_one)
player_sprite.add(player_one)

# init barrier list
barrier_sprites.add(Barrier(container_1, map_current_pos, (402, 180), container_ratio))
barrier_sprites.add(Barrier(container_2, map_current_pos, (502, 280), container_ratio))




# game loop

# built in font and font size
# can turn off these readouts afterwards
font = pygame.font.Font('freesansbold.ttf', 16)

text_resolution = font.render('width: ' + str(map_width()) + ' eight: ' + str(map_height()), True, GREEN, BLACK)
text_refresh= font.render('refresh rate: ' + str(REFRESH_RATE), True, GREEN, BLACK)
text_map_zoom = font.render('map zoom: ' + str(MAP_ZOOM), True, GREEN, BLACK)
text_player_speed = font.render('player speed: ' + str(PLAYER_SPEED), True, GREEN, BLACK)
text_collision = font.render(' Not Touching !', True, RED, BLACK)


# drawing text rect for positioning
text_rect_1 = text_resolution.get_rect()
text_rect_2 = text_refresh.get_rect()
text_rect_3 = text_map_zoom.get_rect()
text_rect_4 = text_player_speed.get_rect()
#text_rect_5 = text_collision.get_rect()

while running:
    # draw sprites
    screen.fill(BLACK)

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

    #if player_one.barrier_top() or player_one.barrier_bottom() or player_one.barrier_left() or player_one.barrier_right():
        #text_collision = font.render(' Touching !', True, GREEN, BLACK)
    #else:
        #text_collision = font.render(' Not Touching !', True, RED, BLACK)

    #screen.blit(text_collision, (text_rect_5.x, text_rect_5.y + 64))

    pygame.display.update()
    # event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        map_sprite.update(key_pressed)

        # screen.blit(pygame.image.load(player_img_name), (0, 0))

        clock.tick(REFRESH_RATE)
        for players in player_sprite:
            players.key_face()
            players.update()
            barrier_sprites.update(key_pressed)

        pygame.display.update()


