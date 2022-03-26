from pygame import *
from random import randint
font.init()

# нам нужны такие картинки:
img_back = "galaxy.jpg"  # фон игры
img_hero = "rocket.png"  # герой
img_enemy = "ufo.png"  # враг
img_bullet = "bullet.png"

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
        bullet = Bullet(img_bullet, self.rect.centerx - 7.5 , self.rect.top, 15, 20, -15)
        bullets.add(bullet)


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


class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed


# Создаём окошко
win_width = 700
win_height = 500
display.set_caption("Shooter")
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_back), (win_width, win_height))

# создаём спрайты
ship = Player(img_hero, 5, win_height - 100, 80, 100, 10)

lost = 0
kill = 0

font1 = font.SysFont('Arial', 38)

counter_lost = font1.render("Пропущено врагов: " + str(lost), True, (231, 45, 98))
counter_kill = font1.render("Уничтожено врагов: " + str(kill), True, (231, 45, 98))
font2 = font.SysFont('Arial', 50)

lose = font2.render("Ви все одно нічого не отримаєте)", True, (255, 50, 30))
win = font2.render("Слава Україні, Іди гуляй, окупанте", True, (255, 50, 30))

monsters = sprite.Group()
for i in range(1, 6):
    monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
    monsters.add(monster)

bullets = sprite.Group()

# переменная "игра закончилась": как только там True, в основном цикле перестают работать спрайты
finish = False
# Основной цикл игры:
run = True  # флаг сбрасывается кнопкой закрытия окна
while run:
    # событие нажатия на кнопку “Закрыть”
    for e in event.get():
        if e.type == QUIT:
            run = False
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                ship.fire()

    if not finish:
        # keys = key.get_pressed()
        # if keys[K_SPACE]:
        #     ship.fire()
        
        # обновляем фон
        window.blit(background, (0, 0))

        # производим движения спрайтов
        ship.update()
        monsters.update()

        bullets.draw(window)
        bullets.update()

        # обновляем их в новом местоположении при каждой итерации цикла
        ship.reset()
        monsters.draw(window)

        counter_lost = font1.render("Пропущено врагов: " + str(lost), True, (231, 45, 98))
        window.blit(counter_lost, (50, 30))
        
        counter_kill = font1.render("Уничтожено врагов: " + str(kill), True, (231, 45, 98))
        window.blit(counter_kill, (400, 30))
        
        gruz200 = sprite.groupcollide(monsters, bullets, False, True)
        for g in gruz200:
            g.rect.x = randint(80, win_width - 80)
            g.rect.y = -50
            kill += 1
            
        privid_Kyieva = sprite.spritecollide(ship, monsters, False)
        for p in privid_Kyieva:
            p.rect.x = randint(80, win_width - 80)
            p.rect.y = -50
            window.blit(lose, (70, 200))
            finish = True
            
        if kill == 10:
            window.blit(win, (70, 200))
            finish = True
        
        if lost > 3:
            window.blit(lose, (70, 200))
            finish = True

        display.update()
    # цикл срабатывает каждую 0.05 секунд
    time.delay(50)