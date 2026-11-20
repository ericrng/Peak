import pygame as pg
import random

from pygame.sprite import collide_rect


def move_pos(obj, x, y):
    obj.x += x
    obj.y += y


class Player(pg.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.rect = pg.Rect(100, 100, 100, 100)
        self.x = x
        self.y = y
        self.rect.center = (x, y)
        self.hp = 100
        self.speed = float(10)
        self.jump_height = 20
        self.coin_count = 0
        self.status = True

    def movement(self):
        dx = 0
        dy = 0
        keys = pg.key.get_pressed()
        # Handling Cardinal Directions
        if keys[pg.K_DOWN]:
            dy += 1
        if keys[pg.K_UP]:
            dy -= 1
        if keys[pg.K_RIGHT]:
            dx += 1
        if keys[pg.K_LEFT]:
            dx -= 1
        if abs(dx) == 1 and abs(dy) == 1:
            dx *= 0.707
            dy *= 0.707
        self.x += dx * self.speed
        self.y += dy * self.speed
        self.rect.center = self.x, self.y

    def status_check(self):
        if self.hp <= 0:
            self.status = False

    def update(self):
        self.movement()
        self.status_check()


class Coin(pg.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.rect = pg.Rect(x, y, 100, 100)
        self.status = False

    def collected(self, player):
        if not self.status and self.rect.colliderect(player.rect):
            self.status = True
            print("Oh no, the coin has been collected!")
            player.coin_count += 1
            self.kill()


class Lava(pg.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.rect = pg.Rect(x, y, 100, 100)
        self.damage = 100
        self.speed = 10

    def rise(self, dt):
        self.rect.centery -= (self.speed * dt)

    def collide_player(self, player, dt):
        if self.rect.colliderect(player.rect):
            print(player.hp)
            player.hp -= self.damage * dt

    def update(self, player, dt):
        self.collide_player(player, dt)
        self.rise(dt)