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

player_img_name = 'survivor-idle_knife_0.png'
player_img = pygame.image.load(player_img_name)



def player_width():
    width = int( player_img.get_rect().size[0]/(map_width()*2) )
    return width


def player_height():
    height = int( player_img.get_rect().size[1]/(map_height()*2) )
    return height

# movement properties
# maybe grab difficulty multiplier here?
player_speed = 1*3 # * difficulty

# WASD inputs
KEYS = {pygame.K_w : (0, 1),
        pygame.K_a : (1, 0),
        pygame.K_s : (0, -1),
        pygame.K_d : (-1, 0)}


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # variables for the class
        self.image = pygame.image.load(player_img_name)
        self.rect = self.image.get_rect()
        self.image = pygame.transform.scale(player_img, (int(map_width() / 8), int(map_height() / 8)))
        self.is_north = False
        self.is_east = True
        self.is_west = False
        self.is_south = False


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
        #self.rect = self.image.get_rect(center=self.rect.center)


    def update(self):


        # pos = pygame.mouse.get_pos()

        # place the character at the center of the screen
        self.rect.x = int(map_width()/2) - int(player_width()/2)
        self.rect.y = int(map_height()/2) - int(player_height()/2)

        self.key_face()
        #self.mouse_face()







# initializes the map and its movement

class Map(pygame.sprite.Sprite):
    def __init__(self, img):
        super().__init__()
        self.image = pygame.image.load(img)
        self.rect = self.image.get_rect()
        self.speed = player_speed
        self.keys = pygame.key.get_pressed()

    def update(self, keys):
        self.image = pygame.transform.scale(map_img, (map_width() * 2, map_height() * 2))
        # movement

        # if the key being pressed is in the array of KEYS
        for key in KEYS:
            if keys[key]:
                # take the value of the tuple and add it do the position
                self.rect.x += KEYS[key][0]*self.speed
                self.rect.y += KEYS[key][1]*self.speed

       #self.rect.clamp_ip(map_img.get_rect())  # Keep player on screen.




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

# init sprites
map_sprite.add(Map(map_img_name))
player_sprite.add(Player())

# adding sprites

while running:
    key_pressed = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False



        # screen.blit(pygame.image.load(player_img_name), (0, 0))
        map_sprite.draw(screen)
        player_sprite.draw(screen)

        clock.tick(60)

        map_sprite.update(key_pressed)
        player_sprite.update()
        pygame.display.update()



