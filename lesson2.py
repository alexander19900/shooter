from pygame import *
from random import randint
font.init()

# нам нужны такие картинки:
img_back = "galaxy.jpg"  # фон игры
img_hero = "rocket.png"  # герой
img_enemy = "ufo.png"  # враг


# класс-родитель для других спрайтов
class GameSprite(sprite.Sprite):
    # конструктор класса
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        # Вызываем конструктор класса (Sprite):
        sprite.Sprite.__init__(self)

        # каждый спрайт должен хранить свойство image - изображение
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed

        # каждый спрайт должен хранить свойство rect - прямоугольник, в который он вписан
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    # метод, отрисовывающий героя на окне
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


# класс главного игрока
class Player(GameSprite):
    # метод для управления спрайтом стрелками клавиатуры
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed

    # метод "выстрел" (используем место игрока, чтобы создать там пулю)
    def fire(self):
        pass


# класс спрайта-врага
class Enemy(GameSprite):
    # движение врага
    def update(self):
        global lost
        self.rect.y += self.speed
        # исчезает, если дойдет до края экрана
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost += 1


# Создаём окошко
win_width = 700
win_height = 500
display.set_caption("Shooter")
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_back), (win_width, win_height))

# создаём спрайты
ship = Player(img_hero, 5, win_height - 100, 80, 100, 10)

lost = 0

font1 = font.Font(None, 38)
counter = font1.render("Пропущено врагов: " + str(lost), True, (231, 45, 98))

monsters = sprite.Group()
for i in range(1, 6):
    monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
    monsters.add(monster)

# переменная "игра закончилась": как только там True, в основном цикле перестают работать спрайты
finish = False
# Основной цикл игры:
run = True  # флаг сбрасывается кнопкой закрытия окна
while run:
    # событие нажатия на кнопку “Закрыть”
    for e in event.get():
        if e.type == QUIT:
            run = False

    if not finish:
        # обновляем фон
        window.blit(background, (0, 0))

        # производим движения спрайтов
        ship.update()
        monsters.update()

        # обновляем их в новом местоположении при каждой итерации цикла
        ship.reset()
        monsters.draw(window)

        counter = font1.render("Пропущено врагов: " + str(lost), True, (231, 45, 98))
        window.blit(counter, (50, 30))

        display.update()
    # цикл срабатывает каждую 0.05 секунд
    time.delay(50)