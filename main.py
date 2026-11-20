import pygame as pg
import sys
import random
from game import move_pos, Player, Coin, Lava

pg.init()
DISPLAY_SIZE = (800,800)
player = Player(100, 100)
coin = Coin(random.randint(1, 800), random.randint(1, 800))
window = pg.display.set_mode(DISPLAY_SIZE)
screen = window.get_rect()
lava = Lava(800, 800)
running = True
clock = pg.time.Clock()
real_time = clock.tick(60)/1000
while running:
    window.fill((255,255,255))
    clock.tick(60)
    keys = pg.key.get_pressed()
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
    if not coin.status:
        coin.collected(player)
        pg.draw.rect(window, (255, 255, 0), coin.rect)
    else:
        coin = Coin(random.randint(1, 800), random.randint(1, 800))
    if player.coin_count > 10:
        player.coin_count -= 10
        player.speed += 2
    lava.update(player, real_time)
    player.update()
    if not player.status:
        running = False
    player.rect.clamp_ip(screen)
    coin.rect.clamp_ip(screen)
    lava.rect.clamp_ip(screen)
    pg.draw.rect(window, (255, 0, 0), player.rect)
    pg.draw.rect(window, (255, 0, 0), lava)
    pg.display.flip()

pg.quit()
sys.exit()