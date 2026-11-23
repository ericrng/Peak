import pygame as pg
import random
import pygame_gui


class Player(pg.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        image = pg.transform.scale(pg.image.load("slime@16x.png").convert_alpha(), (50, 50))
        self.image = image
        self.rect = image.get_rect()
        self.x = x
        self.y = y
        self.rect.center = (x, y)
        self.hp = 100
        self.speed = 10
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
        image = pg.transform.scale(pg.image.load("coin@16x.png").convert_alpha(), (50, 50))
        self.image = image
        self.rect = image.get_rect()
        self.rect.center = (x, y)
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
        self.rect = pg.Rect(x, y, 800, 200)
        self.rect.center = (x, y)
        self.x = x
        self.y = y
        self.damage = 100
        self.speed = 10

    def rise(self, dt):
        self.y -= (self.speed * dt)
        self.rect.center = int(self.x), int(self.y)

    def collide_player(self, player, dt):
        if self.rect.colliderect(player.rect):
            player.hp -= self.damage * dt

    def update(self, player, dt):
        self.rise(dt)
        self.collide_player(player, dt)


def game_loop(window, screen, clock):
    player = Player(400, 400)
    coin = Coin(random.randint(1, 800), random.randint(1, 800))
    lava = Lava(0, 700)
    shop = pg.Rect(0, 1000, 800, 200)
    running = True
    while running:
        window.fill((255, 255, 255))
        clock.tick(60)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return "Quit"
            if event.type == pg.MOUSEBUTTONDOWN:
                if shop.collidepoint(event.pos):
                    if player.coin_count > 10:
                        player.coin_count -= 10
                        player.speed += 2
        if not coin.status:
            coin.collected(player)
            window.blit(coin.image, coin.rect)
        else:
            coin = Coin(random.randint(1, 800), random.randint(1, 800))
        lava.update(player, 1 / 60)
        player.update()
        if not player.status:
            running = False
        player.rect.clamp_ip(screen)
        coin.rect.clamp_ip(screen)
        lava.rect.clamp_ip(screen)
        shop.clamp_ip(window.get_rect())
        window.blit(player.image, player.rect)
        pg.draw.rect(window, (255, 0, 0), lava)
        pg.draw.rect(window, (0,0,0), shop)
        pg.display.flip()
    return "Start Menu"


def start_menu(display_size, dt, running):
    manager = pygame_gui.UIManager(display_size)
    start_button = pygame_gui.elements.UIButton(relative_rect=(0, 600, 800, 200), text="Start", manager=manager)
    settings_button = pygame_gui.elements.UIButton(relative_rect=(0, 800, 800, 200), text="Settings", manager=manager)
    quit_button = pygame_gui.elements.UIButton(relative_rect=(0, 200, 800, 400), text="Quit", manager=manager)
    window = pg.display.set_mode(display_size)
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return "Quit"
            manager.process_events(event)
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == start_button:
                    return "Game Start"
                if event.ui_element == settings_button:
                    settings_menu(display_size, dt, running)
                    return "Settings"
                if event.ui_element == quit_button:
                    return "Quit"
        manager.update(dt)
        window.fill((255,255,255))
        manager.draw_ui(window)
        pg.display.flip()
    return "Quit"


def settings_menu(display_size, dt, running):
    manager = pygame_gui.UIManager(display_size)
    window = pg.display.set_mode(display_size)
    setting_button_1 = pygame_gui.elements.UIButton(relative_rect=(200, 200, 400, 400), text="Placeholder", manager=manager)
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return "Quit"
            manager.process_events(event)
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == setting_button_1:
                    return "Start Menu"
        manager.update(dt)
        manager.draw_ui(window)
        pg.display.flip()
    return "Start Menu"


def platform_generator():
    platform = pg.Rect(800, 800, 200, 200)
    ladder = pg.Rect(600, 800, 25, 200)