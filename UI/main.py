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
YELLOW = (255, 255, 0)

# Directions
NORTH = 0
SOUTH = 1
EAST = 2
WEST = 3

# settings
REFRESH_RATE = 60
MAP_ZOOM = 1
FONT = 32
# movement properties
# maybe grab difficulty multiplier here?
PLAYER_SPEED = 100 # * difficulty

TRUE = 1
FALSE = 0

# load map branch
pygame.init()

# grab the map image from the main manu
# from main_menu import map_img_name
# aa why is not importing the image :(
# put current, resource, and image path into the main menu function 20201119
map_img_name = 'Map_Final.png'

# grab the player image from the main menu
# from main_menu import player_img_name

character_ratio = (28, 28)
player_img_name = 'survivor-idle_knife_0.png'

enemy_img_name = 'skeleton_idle_6.png'

# barrier sprites
# container_1
container_ratio = (6, 12)
container_1 = 'container_1.png'
container_3 = 'container_3.png'

box_ratio = (28, 24)
box_1 = 'wood_box_1.png'

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
icon_img_name = 'skeleton_idle_6.png'
icon_img = pygame.image.load(icon_img_name)
pygame.display.set_icon(icon_img)

# window  update
pygame.display.flip()

# WASD inputs
KEYS = {pygame.K_w: (0, -1),
        pygame.K_a: (-1, 0),
        pygame.K_s: (0, 1),
        pygame.K_d: (1, 0)}


# class for player
# takes player img filename
class Player(pygame.sprite.Sprite):
    def __init__(self, img_name):
        super().__init__()
        self.image = pygame.image.load(img_name)
        self.rect = self.image.get_rect()

        # scaling the image to fit the map
        self.image = pygame.transform.scale(self.image, (int(map_width() / (MAP_ZOOM * character_ratio[0])),
                                                         int(map_height() / (MAP_ZOOM * character_ratio[1]))))
        self.rect.width = int(map_width() / (MAP_ZOOM * character_ratio[0]))
        self.rect.height = int(map_height() / (MAP_ZOOM * character_ratio[0]))

        self.rect.x = 75
        self.rect.y = 75

        self.speed = PLAYER_SPEED / 50

        # for direction facing
        self.is_north = False
        self.is_east = True
        self.is_west = False
        self.is_south = False

        self.collision_top = False
        self.collision_sides = False

        self.score = 0;

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
    def key_face(self, event):
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
            elif event.key == pygame.K_s:
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
            elif event.key == pygame.K_a:
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
            elif event.key == pygame.K_d:
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

    def player_width(self):
        width = int(self.image.get_rect().size[0] / (map_width() * 2))
        return width

    def player_height(self):
        height = int(self.image.get_rect().size[1] / (map_height() * 2))
        return height

    def move(self, keys):
        # movement
        dx = 0
        dy = 0

        Maps = map_sprite
        padding = 5

        # x direction
        for x in KEYS:
            if keys[x]:
                dx += (KEYS[x][0] * self.speed)

        barrier_collision_list = pygame.sprite.spritecollide(self, barrier_sprites, False)

        for barrier in barrier_collision_list:
            # left side touching right side of barrier
            if dx < 0:
                self.rect.left = barrier.rect.right + padding
            elif dx > 0:
                self.rect.right = barrier.rect.left - padding
        # y direction
        for x in KEYS:
            if keys[x]:
                dy += (KEYS[x][1] * self.speed)

        for barrier in barrier_collision_list:
            if dy < 0:
                self.rect.top = barrier.rect.bottom + padding
            elif dy > 0:
                self.rect.bottom = barrier.rect.top - padding

        for maps in Maps:
            if maps.rect.top > self.rect.top:
                self.collision_top = True
                self.rect.top = maps.rect.top
            if maps.rect.bottom < self.rect.bottom:
                self.collision_top = True
                self.rect.bottom = maps.rect.bottom
            if maps.rect.left > self.rect.left:
                self.collision_sides = True
                self.rect.left = maps.rect.left
            if maps.rect.right < self.rect.right:
                self.collision_sides = True
                self.rect.right = maps.rect.right

            self.rect.x += dx
            self.rect.y += dy

    def coin_collect(self):
        player_collision_list = pygame.sprite.groupcollide(coin_sprites, player_sprite, True, False)
        self.score = 0

        for x in player_collision_list:
            self.score += 10000

        return self.score

    def enemy_encounter(self):
        enemy_collision_list = pygame.sprite.groupcollide(enemy_sprites, player_sprite, False, True)
        for x in enemy_collision_list:
            return FALSE

    def pos(self):
        return self.rect

    def update(self, keys):
        self.move(keys)
        # uncomment for hit box
        # pygame.draw.rect(screen, GREEN, (self.rect.x, self.rect.y, self.rect.width, self.rect.height), 0)


class Enemy(pygame.sprite.Sprite):
    def __init__(self, img_name, spawn_x, spawn_y):
        super().__init__()
        self.image = pygame.image.load(img_name)
        self.rect = self.image.get_rect()

        # scaling the image to fit the map
        self.image = pygame.transform.scale(self.image,
                                            (int(map_width() / (MAP_ZOOM * character_ratio[0])),
                                             int(map_height() / (MAP_ZOOM * character_ratio[1]))))
        self.rect.width = int(map_width() / (MAP_ZOOM * character_ratio[0]))
        self.rect.height = int(map_height() / (MAP_ZOOM * character_ratio[1]))

        self.speed = PLAYER_SPEED / 100

        # for direction facing
        self.is_north = False
        self.is_east = True
        self.is_west = False
        self.is_south = False

        self.dx = 0
        self.dy = 0

        self.rect.x = spawn_x
        self.rect.y = spawn_y

    # moves to the player's position
    def moveto(self, player_pos):
        self.dx = 0
        self.dy = 0
        if self.rect.x < player_pos[0]:
            self.dx += self.speed

        if self.rect.x > player_pos[0]:
            self.dx -= self.speed

        if self.rect.y < player_pos[1]:
            self.dy += self.speed

        if self.rect.y > player_pos[1]:
            self.dy -= self.speed

        self.rect.x += self.dx
        self.rect.y += self.dy

    def barrier(self):
        padding = 2

        barrier_collision_list = pygame.sprite.spritecollide(self, barrier_sprites, False)

        for barrier in barrier_collision_list:
            # left side touching right side of barrier
            if self.dx < 0:
                # if encountered, move laterally
                self.dy += 5
                self.rect.x += 2
            # right side touching left side of barrier
            elif self.dx > 0:
                self.dy -= 5
                self.rect.x -= 2
            # top side touching bottom of barrier
            elif self.dy < 0:
                self.dx += 5
                self.rect.y -= 2
            # bottom side touching top of barrier
            elif self.dy > 0:
                self.dx -= 5
                self.rect.y += 2

            self.rect.x += self.dx
            self.rect.y += self.dy

        self.dx = 0
        self.dy = 0

        for maps in map_sprite:
            if maps.rect.top > self.rect.top:
                self.rect.top = maps.rect.top
            if maps.rect.bottom < self.rect.bottom:
                self.rect.bottom = maps.rect.bottom
            if maps.rect.left > self.rect.left:
                self.rect.left = maps.rect.left
            if maps.rect.right < self.rect.right:
                self.rect.right = maps.rect.right

    # similar in function the player keyface, but is not controlled by keys
    def key_face(self):

        if self.dy < 0:
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

        # face down
        if self.dy > 0:
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
        if self.dx < 0:
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
        if self.dx > 0:
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

    def update(self, player_pos):
        self.moveto(player_pos)
        self.barrier()
        self.key_face()


class Coins(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        self.image = pygame.Surface((20, 20))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = y

    def barrier(self):
        barrier_collision_list = pygame.sprite.spritecollide(self, barrier_sprites, False)

        for barrier in barrier_collision_list:

            self.rect.x += 5
            self.rect.y += 5

        for maps in map_sprite:
            if maps.rect.top > self.rect.top:
                self.rect.top = maps.rect.top
            if maps.rect.bottom < self.rect.bottom:
                self.rect.bottom = maps.rect.bottom
            if maps.rect.left > self.rect.left:
                self.rect.left = maps.rect.left
            if maps.rect.right < self.rect.right:
                self.rect.right = maps.rect.right

    def update(self):
        self.barrier()


# Class for any barrier elements, (walls, boxes, containers, etc)
# takes the barrier image,tuple position on the map, and the current position of the map.
class Barrier(pygame.sprite.Sprite):
    def __init__(self, img_name, place_xy, ratio_xy):
        super().__init__()

        self.image = pygame.image.load(img_name)
        self.rect = self.image.get_rect()

        self.image = pygame.transform.scale(self.image,
                                            (int(map_width() / (MAP_ZOOM * ratio_xy[0])),
                                             int(map_height() / (MAP_ZOOM * ratio_xy[1]))))
        self.rect.width = (int(map_width() / (MAP_ZOOM * ratio_xy[0])))
        self.rect.height = (int(map_height() / (MAP_ZOOM * ratio_xy[1])))

        self.map_center_x = int(map_width() / 2)
        self.map_center_y = int(map_height() / 2)


        # initial placement at the start of the level
        self.rect.left = place_xy[0] * MAP_ZOOM
        self.rect.top = place_xy[1] * MAP_ZOOM

    def update(self, keys):
        # refreshed placement as the player moves
        self.rect
        pygame.draw.rect(screen, RED, (self.rect.x, self.rect.y, self.rect.width, self.rect.height), 0)

# initializes the map and its movement
class Map(pygame.sprite.Sprite):
    def __init__(self, img):
        super().__init__()
        self.image = pygame.image.load(img)
        # for the zoomed in map
        # self.image = pygame.transform.scale(self.image, (int(map_width() * MAP_ZOOM), int(map_height() * MAP_ZOOM)))
        self.rect = self.image.get_rect()

    def current_pos(self):
        current_pos = (self.rect.x, self.rect.y)
        return current_pos

    def update(self, keys):
        self.rect

# level init
clock = pygame.time.Clock()

# sprite variables
map_sprite = pygame.sprite.Group()
player_sprite = pygame.sprite.Group()
barrier_sprites = pygame.sprite.Group()
enemy_sprites = pygame.sprite.Group()
coin_sprites = pygame.sprite.Group()

# main game functions
def menu():


    font = pygame.font.Font('freesansbold.ttf', 32)

    # text stuffs
    title = font.render('Welcome to Sneaky Beaky (the game)', True, BLACK, WHITE)
    how_to = font.render('\'P\'for procedural game, \'Enter\' for default game', True, RED, WHITE)
    how_to_2 = font.render('CPSC 100 Lab Section L1M', True, RED, WHITE)

    made_by = font.render('Made by Group 82:', True, BLUE, WHITE)
    name_1 = font.render('Elijah Cuico 21233069', True, BLUE, WHITE)
    name_2 = font.render('Viktor Moreno 75388181', True, BLUE, WHITE)
    title_rect = title.get_rect()
    how_to_rect = how_to.get_rect()
    running = True

    while running:

        screen.fill(GRAY)
        screen.blit(title, (int(map_height() / 2) - int(title_rect.width/2) + 140, 100))
        screen.blit(how_to, (int(map_height() / 2) - int(how_to_rect.width/2) + 140, 200))
        screen.blit(how_to_2, (int(map_height() / 2) - int(title_rect.width / 2) + 230 , 300))
        screen.blit(made_by, (int(map_height() / 2) - int(title_rect.width / 2), 370))
        screen.blit(name_1, (int(map_height() / 2) - int(title_rect.width / 2), 440))
        screen.blit(name_2, (int(map_height() / 2) - int(title_rect.width / 2), 510))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    pygame.display.flip()
                    procedural_game()
                    running = False
                if event.key == pygame.K_RETURN:
                    pygame.display.flip()
                    default_game()
                    running = False
                if event.key == pygame.K_ESCAPE:
                    pygame.display.flip()
                    running = False

        pygame.display.update()



# loads Map_Final
def default_game():
    map_sprite.empty()
    player_sprite.empty()
    barrier_sprites.empty()
    enemy_sprites.empty()
    coin_sprites.empty()

    pygame.display.flip()

    # giving class Player the list of barriers to use in collision check
    player_sprite.barriers = barrier_sprites

    # init sprites
    map_one = Map(map_img_name)
    player_one = Player(player_img_name)
    enemy_one = Enemy(enemy_img_name, int(map_width() /2), int(map_height() /2))

    random.seed(time.time())

    x = 0

    # change this for number of coins
    while x < 20:
        random_x = random.randint(0, map_width())
        random_y = random.randint(100, map_height())
        coins = Coins(random_x, random_y)
        coin_sprites.add(coins)
        x += 1

    # add sprites
    map_sprite.add(map_one)
    player_sprite.add(player_one)

    x = 0

    # init enemy list
    enemy_sprites.add(enemy_one)

    # init barrier list
    # containers
    barrier_sprites.add(Barrier(container_1, (385, 130), container_ratio))
    barrier_sprites.add(Barrier(container_1, (385, 210), container_ratio))
    barrier_sprites.add(Barrier(container_3, (385, 297), container_ratio))

    # building 1
    barrier_sprites.add(Barrier(box_1, (180, 375), box_ratio))
    barrier_sprites.add(Barrier(box_1, (220, 375), box_ratio))
    barrier_sprites.add(Barrier(box_1, (230, 455), box_ratio))
    barrier_sprites.add(Barrier(box_1, (270, 455), box_ratio))
    barrier_sprites.add(Barrier(box_1, (270, 495), box_ratio))
    barrier_sprites.add(Barrier(box_1, (270, 565), box_ratio))
    barrier_sprites.add(Barrier(box_1, (220, 525), box_ratio))
    barrier_sprites.add(Barrier(box_1, (230, 605), box_ratio))
    barrier_sprites.add(Barrier(box_1, (270, 605), box_ratio))
    barrier_sprites.add(Barrier(box_1, (180, 605), box_ratio))

    # building 2
    barrier_sprites.add(Barrier(box_1, (425, 467), box_ratio))  # right column
    barrier_sprites.add(Barrier(box_1, (425, 500), box_ratio))
    barrier_sprites.add(Barrier(box_1, (425, 530), box_ratio))

    barrier_sprites.add(Barrier(box_1, (390, 467), box_ratio))  # left column
    barrier_sprites.add(Barrier(box_1, (390, 500), box_ratio))
    barrier_sprites.add(Barrier(box_1, (390, 530), box_ratio))

    barrier_sprites.add(Barrier(box_1, (485, 585), box_ratio))

    barrier_sprites.add(Barrier(box_1, (525, 515), box_ratio))
    barrier_sprites.add(Barrier(box_1, (560, 515), box_ratio))
    barrier_sprites.add(Barrier(box_1, (560, 550), box_ratio))

    barrier_sprites.add(Barrier(box_1, (615, 515), box_ratio))
    barrier_sprites.add(Barrier(box_1, (615, 480), box_ratio))

    barrier_sprites.add(Barrier(box_1, (615, 480), box_ratio))

    barrier_sprites.add(Barrier(box_1, (735, 465), box_ratio))

    barrier_sprites.add(Barrier(box_1, (735, 570), box_ratio))
    barrier_sprites.add(Barrier(box_1, (735, 605), box_ratio))
    barrier_sprites.add(Barrier(box_1, (700, 605), box_ratio))

    # building 3
    barrier_sprites.add(Barrier(box_1, (770, 115), box_ratio))
    barrier_sprites.add(Barrier(box_1, (805, 115), box_ratio))

    barrier_sprites.add(Barrier(box_1, (770, 185), box_ratio))

    barrier_sprites.add(Barrier(box_1, (770, 290), box_ratio))
    barrier_sprites.add(Barrier(box_1, (770, 325), box_ratio))
    barrier_sprites.add(Barrier(box_1, (805, 290), box_ratio))
    barrier_sprites.add(Barrier(box_1, (805, 255), box_ratio))

    barrier_sprites.add(Barrier(box_1, (860, 215), box_ratio))
    barrier_sprites.add(Barrier(box_1, (860, 355), box_ratio))

    running = True
    TOTAL_SCORE = 0
    TIME_START = time.time()

    # built in font and font size
    # can turn off these readouts afterwards
    font = pygame.font.Font('freesansbold.ttf', 16)

    text_resolution = font.render('width: ' + str(map_width()) + ' eight: ' + str(map_height()), True, GREEN, BLACK)
    text_refresh = font.render('WASD to move, dont let the enemies touch you!', True, GREEN, BLACK)
    text_map_zoom = font.render('You can warp through boxes! (if you can figure out how)', True, GREEN, BLACK)
    # text_player_speed = font.render('Score: ' + str(SCORE), True, GREEN, BLACK)
    # text_collision = font.render(' offset y: ' + str(barrier_sprites[0].collision_offset_y()), True, GREEN, BLACK)

    # drawing text rect for positioning
    text_rect_1 = text_resolution.get_rect()
    text_rect_2 = text_refresh.get_rect()
    text_rect_3 = text_map_zoom.get_rect()

    # text_rect_5 = text_collision.get_rect()
    SCORE = 20000

    while running:
        # score and time keeping
        pygame.display.update()
        TIME_CURR = time.time()
        dt = TIME_CURR - TIME_START
        time_bonus = (10 / dt)
        # the more time spent, the lower the time bonus is

        SCORE -= time_bonus

        screen.fill(BLACK)

        for players in player_sprite:
            enemy_sprites.update(players.pos())
            SCORE += players.coin_collect()
            players.enemy_encounter()
            if len(player_sprite.sprites()) == 0:
                TOTAL_SCORE = SCORE
                running = False
            if len(coin_sprites.sprites()) == 0:
                TOTAL_SCORE = SCORE
                running = False


        # draw sprites
        map_sprite.draw(screen)
        player_sprite.draw(screen)
        enemy_sprites.draw(screen)

        coin_sprites.draw(screen)
        for x in coin_sprites:
            x.update()

        barrier_sprites.draw(screen)

        text_score = font.render('Score: ' + str(int(SCORE)), True, GREEN, BLACK)
        text_time = font.render('Time: ' + str(int(dt)), True, GREEN, BLACK)
        text_rect_4 = text_score.get_rect()
        text_rect_5 = text_time.get_rect()

        key_pressed = pygame.key.get_pressed()

        # where the actual movement is, should be outside of the event loop
        #barrier_sprites.update(key_pressed)
        #map_sprite.update(key_pressed)


        screen.blit(text_resolution, text_rect_1)
        screen.blit(text_refresh, (text_rect_2.x, text_rect_2.y + 16))
        screen.blit(text_map_zoom, (text_rect_3.x, text_rect_3.y + 32))
        screen.blit(text_score, (text_rect_4.x, text_rect_4.y + 53))
        screen.blit(text_time, (text_rect_5.x, text_rect_5.y + 70))

        # event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                TOTAL_SCORE = SCORE
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.display.flip()
                    running = False

            clock.tick(REFRESH_RATE)
            player_sprite.update(key_pressed)

            for players in player_sprite:
                players.key_face(event)

        player_sprite.update(key_pressed)
        pygame.display.update()

    running = True

    # game over thread
    while running:


        font = pygame.font.Font('freesansbold.ttf', 32)

        pygame.display.update()

        game_over = font.render('GAME OVER', True, RED, WHITE)
        final_score = font.render('Score: ' + str(int(TOTAL_SCORE)), True, RED, WHITE)
        how_to_2 = font.render('\'P\'for procedural game, \'Enter\' for default game', True, RED, WHITE)
        made_by = font.render('Made by Group 82:', True, BLUE, WHITE)
        name_1 = font.render('Elijah Cuico 21233069', True, BLUE, WHITE)
        name_2 = font.render('Viktor Moreno 75388181', True, BLUE, WHITE)

        game_over_rect = game_over.get_rect()

        screen.blit(game_over, (int(map_height() / 2) - int(game_over_rect.width / 2) + 140, 100))
        screen.blit(final_score, (int(map_height() / 2) - int(game_over_rect.width / 2) + 140, 200))
        screen.blit(how_to_2, (int(map_height() / 2) - int(game_over_rect.width / 2) - 100, 300))
        screen.blit(made_by, (int(map_height() / 2) - int(game_over_rect.width / 2), 370))
        screen.blit(name_1, (int(map_height() / 2) - int(game_over_rect.width / 2), 440))
        screen.blit(name_2, (int(map_height() / 2) - int(game_over_rect.width / 2), 510))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    pygame.display.flip()
                    procedural_game()
                    running = False
                if event.key == pygame.K_RETURN:
                    pygame.display.flip()
                    default_game()
                    running == False
                if event.key == pygame.K_ESCAPE:
                    TOTAL_SCORE = SCORE
                    pygame.display.flip()
                    running = False

# level init
new_clock = pygame.time.Clock()

def procedural_game():
    map_sprite.empty()
    player_sprite.empty()
    barrier_sprites.empty()
    enemy_sprites.empty()
    coin_sprites.empty()

    pygame.display.flip()

    # init sprites
    map_final = Map(map_img_name)
    player_one = Player(player_img_name)

    map_sprite.add(map_final)
    player_sprite.add(player_one)

    random.seed(time.time())

    x = 0

    # change this for number of coins
    while x < 20:
        random_x = random.randint(0, map_width())
        random_y = random.randint(100, map_height())
        coins = Coins(random_x, random_y)
        coin_sprites.add(coins)
        x += 1

    x = 0
    # change this for number of boxes
    while x < 20:
        random_x = random.randint(0, map_width())
        random_y = random.randint(100, map_height())

        random_box = Barrier(box_1, (random_x, random_y), box_ratio)
        random_box_2 = Barrier(box_1, (random_x, random_y), box_ratio)
        random_box_3 = Barrier(box_1, (random_x, random_y), box_ratio)

        # L shape
        if random_x % 3 == 0:
            random_box = Barrier(box_1, (random_x, random_y), box_ratio)
            random_box_2 = Barrier(box_1, (random_x, random_y + 30), box_ratio)
            random_box_3 = Barrier(box_1, (random_x - 30, random_y), box_ratio)
        # v shape
        elif random_x % 6 == 0:
            random_box = Barrier(box_1, (random_x, random_y), box_ratio)
            random_box_2 = Barrier(box_1, (random_x -30, random_y - 30), box_ratio)
            random_box_3 = Barrier(box_1, (random_x + 30, random_y - 30), box_ratio)
        # line shape
        elif random_y % 2 == 0:
            random_box = Barrier(box_1, (random_x, random_y), box_ratio)
            random_box_2 = Barrier(box_1, (random_x, random_y + 30), box_ratio)
            random_box_3 = Barrier(box_1, (random_x , random_y- 30), box_ratio)

        barrier_sprites.add(random_box)
        barrier_sprites.add(random_box_2)
        barrier_sprites.add(random_box_3)
        x += 1

    x = 0
    # Multiple enemies at random spots
    while x < 5:
        random_x = random.randint(0, map_width())
        random_y = random.randint(100, map_height())
        enemy_one = Enemy(enemy_img_name, random_x, random_y)
        enemy_sprites.add(enemy_one)
        x += 1

    pygame.display
    running = True
    TOTAL_SCORE = 0
    TIME_START = time.time()

    # built in font and font size
    # can turn off these readouts afterwards
    font = pygame.font.Font('freesansbold.ttf', 16)

    text_resolution = font.render('width: ' + str(map_width()) + ' eight: ' + str(map_height()), True, GREEN, BLACK)
    text_refresh = font.render('WASD to move, dont let the enemies touch you!', True, GREEN, BLACK)
    text_map_zoom = font.render('You can warp through boxes! (if you can figure out how)', True, GREEN, BLACK)
    # text_player_speed = font.render('Score: ' + str(SCORE), True, GREEN, BLACK)
    # text_collision = font.render(' offset y: ' + str(barrier_sprites[0].collision_offset_y()), True, GREEN, BLACK)

    # drawing text rect for positioning
    text_rect_1 = text_resolution.get_rect()
    text_rect_2 = text_refresh.get_rect()
    text_rect_3 = text_map_zoom.get_rect()

    # text_rect_5 = text_collision.get_rect()
    SCORE = 20000

    while running:
        # score and time keeping
        pygame.display.update()
        TIME_CURR = time.time()
        dt = TIME_CURR - TIME_START
        time_bonus = (10 / dt)
        # the more time spent, the lower the time bonus is

        SCORE -= time_bonus



        for players in player_sprite:
            enemy_sprites.update(players.pos())
            SCORE += players.coin_collect()
            players.enemy_encounter()
            if len(player_sprite.sprites()) == 0:
                TOTAL_SCORE = SCORE
                running = False
            if len(coin_sprites.sprites()) == 0:
                TOTAL_SCORE = SCORE
                running = False

        # draw sprites
        map_sprite.draw(screen)
        screen.fill(GRAY)
        player_sprite.draw(screen)
        enemy_sprites.draw(screen)

        coin_sprites.draw(screen)
        for x in coin_sprites:
            x.update()

        barrier_sprites.draw(screen)

        text_score = font.render('Score: ' + str(int(SCORE)), True, GREEN, BLACK)
        text_time = font.render('Time: ' + str(int(dt)), True, GREEN, BLACK)
        text_rect_4 = text_score.get_rect()
        text_rect_5 = text_time.get_rect()

        key_pressed = pygame.key.get_pressed()

        # where the actual movement is, should be outside of the event loop
        # old code for the inversed mode, didn't work out so well
        # barrier_sprites.update(key_pressed)
        # map_sprite.update(key_pressed)

        screen.blit(text_resolution, text_rect_1)
        screen.blit(text_refresh, (text_rect_2.x, text_rect_2.y + 16))
        screen.blit(text_map_zoom, (text_rect_3.x, text_rect_3.y + 32))
        screen.blit(text_score, (text_rect_4.x, text_rect_4.y + 53))
        screen.blit(text_time, (text_rect_5.x, text_rect_5.y + 70))

        # event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                TOTAL_SCORE = SCORE
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    TOTAL_SCORE = SCORE
                    pygame.display.flip()
                    running = False

            clock.tick(REFRESH_RATE)
            player_sprite.update(key_pressed)

            for players in player_sprite:
                players.key_face(event)

        player_sprite.update(key_pressed)
        pygame.display.update()

    running = True

    # game over thread
    while running:


        font = pygame.font.Font('freesansbold.ttf', 32)

        pygame.display.update()

        game_over = font.render('GAME OVER', True, RED, WHITE)
        final_score = font.render('Score: ' + str(int(TOTAL_SCORE)), True, RED, WHITE)
        how_to_2 = font.render('Thanks for playing!', True, RED, WHITE)
        play_again = font.render('\'P\'for procedural game, \'Enter\' for default game', True, RED, WHITE)
        made_by = font.render('Made by Group 82:', True, BLUE, WHITE)
        name_1 = font.render('Elijah Cuico 21233069', True, BLUE, WHITE)
        name_2 = font.render('Viktor Moreno 75388181', True, BLUE, WHITE)

        play_again_rect = play_again.get_rect()
        game_over_rect = game_over.get_rect()

        screen.blit(game_over, (int(map_height() / 2) - int(game_over_rect.width / 2) + 140, 100))
        screen.blit(final_score, (int(map_height() / 2) - int(game_over_rect.width / 2) + 140, 200))
        screen.blit(how_to_2, (int(map_height() / 2) - int(game_over_rect.width / 2) + 90, 250))
        screen.blit(play_again, (int(map_height() / 2) - int(play_again_rect.width / 2) + 140, 300))
        screen.blit(made_by, (int(map_height() / 2) - int(game_over_rect.width / 2), 370))
        screen.blit(name_1, (int(map_height() / 2) - int(game_over_rect.width / 2), 440))
        screen.blit(name_2, (int(map_height() / 2) - int(game_over_rect.width / 2), 510))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    pygame.display.flip()
                    procedural_game()
                    running = False
                if event.key == pygame.K_RETURN:
                    pygame.display.flip()
                    default_game()
                    running = False
                if event.key == pygame.K_ESCAPE:
                    pygame.display.flip()
                    running = False


# game activation
menu()
pygame.quit()
