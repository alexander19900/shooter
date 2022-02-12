import pygame as pg
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


window = pg.display.set_mode((700, 500))
background = pg.transform.scale(pg.image.load('1200px-MarvelLogo.svg.png'), (700, 500))

clock = pg.time.Clock()

game = True

player = Player("dc_logo.jpg", 300, 430, 10)

while game:
    for _ in pg.event.get():
        if _.type == pg.QUIT:
            game = False

    window.blit(background, (0, 0))

    player.reset()
    player.move()

    pg.display.update()
    clock.tick(60)