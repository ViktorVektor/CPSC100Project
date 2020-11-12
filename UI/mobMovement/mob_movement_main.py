import pygame

#from main import position

class Mob(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.wobs
        pygame.sprite.Sprite.__init__(self,self.groups)
        self.image = MOB_IMG
        self.rect = self.image.get_rect()
        self.pos = vec(x,y) * [INSERT_BY_LOCATION]
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.rect.centre = self.pos
        self.rot = 0

    def update(self):
        self.rot = (self.game.player.pos - self.pos).angle_to(vec(1,0))
        self.image = pg.transform.rotate(self.game.mob_img,self.rot)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.acc = vec(MOB_SPEED, 0).rotate(-self.rot)
        self.acc +=self.vel * -1
        self.vel += self.acc * self.game.dt
        self.pos += self.vel *self.game.dt + 0.5 * self.acc * self.game.dt ** 2
        self.rect.center = self.pos