import pygame as pg
import random
pg.init()


class GameSprite(pg.sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__()
        self.image = pg.transform.scale(pg.image.load(player_image), (65, 65))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


class Player(GameSprite):
    def move(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        elif keys[pg.K_RIGHT] and self.rect.x < 630:
            self.rect.x += self.speed


class Enemy(GameSprite):
    def fall(self):
        self.rect.y += self.player_speed
        if self.rect.y > HEIGHT:
            self.rect.y = 0
            self.rect.x = random.randint(50, WIDTH - 50)


WIDTH = 700
HEIGHT = 500

enemies = pg.sprite.Group()

for i in range(5):
    enemy = Enemy("ufo.png", random.randint(50, WIDTH - 50), -50, random.randint(1, 5))
    enemies.add(enemy)

window = pg.display.set_mode((700, 500))
background = pg.transform.scale(pg.image.load('galaxy.jpg'), (WIDTH, HEIGHT))

clock = pg.time.Clock()

game = True

player = Player("rocket.png", 300, 430, 10)

while game:
    for _ in pg.event.get():
        if _.type == pg.QUIT:
            game = False

    window.blit(background, (0, 0))

    enemies.fall()
    enemies.draw(window)

    player.reset()
    player.move()

    pg.display.update()
    clock.tick(60)