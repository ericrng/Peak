import pygame as pg
import sys
import random
from game import Player, Coin, Lava, start_menu, game_loop, settings_menu

# Initialization
pg.init()

DISPLAY_SIZE = (800, 1000)
window = pg.display.set_mode(DISPLAY_SIZE)
screen = pg.Rect(0, 0, 800, 800)
clock = pg.time.Clock()


game_state = "Start Menu"
while game_state != "Quit":
    if game_state == "Start Menu":
        game_state = start_menu(display_size=DISPLAY_SIZE, dt=clock.tick(60)/1000, running=True)
    elif game_state == "Game Start":
        game_state = game_loop(window, screen, clock)
    elif game_state == "Settings":
        game_state = settings_menu(DISPLAY_SIZE, clock.tick(60)/1000, True)


pg.quit()
sys.exit()