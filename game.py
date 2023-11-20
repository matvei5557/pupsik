import pygame as pg
from sql_bd import DateBaseSQL
import random
pg.init()
apl = pg.image.load('apl.png')
a = pg.image.load('sh.jpg')
pga = pg.image.load('O.jpg')
sound1 = pg.mixer.music.load("foot.mp3")
font_name = pg.font.match_font('arial')  # поиск шифта arial
size = 18  # размер шрифта
W, H = 600, 600
win = pg.display.set_mode((W, H))  # переменная чтобы создать игровое окно
name = ' '

class Apple(pg.sprite.Sprite):
    def __init__(self, x, y):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load('apl.png')
        self.rect = self.image.get_rect()
        self.rect.centerx = random.randrange(0, 570)
        self.rect.bottom = random.randrange(0, 570)

    def new_pos(self):
        self.rect.x = random.randrange(0, 570)
        self.rect.y = random.randrange(0, 570)


class Player(pg.sprite.Sprite):
    def __init__(self, x, y):
        pg.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.speed_x = 1
        self.speed_y = 0
        self.image = pg.image.load('po.jpg')
        self.image = pg.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        if cellision:
            self.rect.x += self.speed_x * 40
            self.rect.y += self.speed_y * 40
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        key = pg.key.get_pressed()
        if key[pg.K_LEFT]:
            if self.speed_x == 0:
                self.speed_x = -1
                self.speed_y = 0
            for tail in tail_sprites.sprites():
                tail.append_direction([{0}], [{1}])
        if key[pg.K_RIGHT]:
            if self.speed_x == 0:
                self.speed_x = 1
                self.speed_y = 0
                for tail in tail_sprites.sprites():
                    tail.append_direction([{1}], [{1}])
        if key[pg.K_UP]:
            if self.speed_y == 0:
                self.speed_x = 0
                self.speed_y = -1
            for tail in tail_sprites.sprites():
                tail.append_direction([{1}], [{1}])
        if key[pg.K_DOWN]:
            if self.speed_y == 0:
                self.speed_x = 0
                self.speed_y = 1
            for tail in tail_sprites.sprites():
                tail.append_direction([{0}], [{1}])


class Tail(pg.sprite.Sprite):
    def __init__(self, event=None, *group):
        super().__init__(*group)
        self.speed_x = player.speed_x
        self.speed_y = player.speed_y
        self.image = pg.image.load('po.jpg')
        self.image = pg.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.x = player.rect.x
        self.rect.y = player.rect.y
        self.direction_list = []
        self.step = 0

    def update(self):
        if self.direction_list != [] and self.step < len(self.direction_list):
            if self.direction_list[self.step][1] == [self.rect.x, self.rect.y]:
                self.speed_x = self.direction_list[self.step][0][0]
                self.speed_y = self.direction_list[self.step][0][1]
                self.step += 1
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

    def append_direction(self, dir, pos):
        self.direction_list.append([dir, pos])
        self.update()


cellision = False
all_sprites = pg.sprite.Group()
apple = Apple(50, 50)
apple_sprites = pg.sprite.Group()
apple_sprites.add(apple)
tail_sprites = pg.sprite.Group()
player = Player(300, 300)
all_sprites.add(player)


def draw_text(surf, text, x, y, size=size, color=(255, 255, 255)):
    font = pg.font.Font(font_name, size)  # определяет шрифт
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


def user_name(surf, text, x, y, size, color=(255, 255, 255)):
    font = pg.font.Font(font_name, size)  # определяет шрифт
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

clock = pg.time.Clock()
mainloop = True
while mainloop:
    for i in pg.event.get():
        if i.type == pg.QUIT:
            exit()
        elif i.type == pg.KEYDOWN:
            if i.key == pg.K_BACKSPACE:
                name = name[:-1]
            elif i.key == pg.K_RETURN:
                mainloop = False
            else:
                name += i.unicode
        win.fill((0, 0, 0))
        win.blit(a, (0, 0))
        draw_text(win, 'Введите имя:', W // 2, H // 2)
        draw_text(win, name, W // 2, H // 2 + 20)
        pg.display.update()
score = 0
while 1:
    for i in pg.event.get():
        if i.type == pg.QUIT:
            exit()
    win.fill((0, 0, 0))
    win.blit(pga, (0, 0))
    all_sprites.update()
    all_sprites.draw(win)
    clock.tick(60)
    str(score)
    collision = pg.sprite.spritecollide(player,apple_sprites,False,pg.sprite.collide_mask)
    happy_end = pg.sprite.spritecollide(player,tail_sprites,False,pg.sprite.collide_mask)
    if happy_end:
        break


    for vertic in range(0, 600, 20):
        pg.draw.line(win, (255, 0, 0), (0, vertic), (600, vertic))
    for horiz in range(0, 600, 20):
        pg.draw.line(win, (0, 255, 0), (horiz, 0), (horiz, 600))
    draw_text(win, name, W // 2, 10, color=(255, 0, 0))
    draw_text(win, str(score), W // 6, 10, color=(0, 0, 255))
    all_sprites.update()
    all_sprites.draw(win)
    apple_sprites.update()
    apple_sprites.draw(win)
    if score != 0:
        tail_sprites.update()
        tail_sprites.draw(win)
    collision = pg.sprite.spritecollide(player, apple_sprites, False, pg.sprite.collide_mask)
    if collision:
        score += 1
        apple.new_pos()
        Tail(tail_sprites)
    pg.display.update()

SQL.set(name, score)
while 1:
    for i in pg.event.get():
        if i.type == pg.QUIT:
            exit()

    win.fill(BLACK)
    offset = 20
    step = 0
    for u_name, u_score in SQL.get():
        step += 1
        draw_text(win, (f'{u_name}: {u_score}'), W // 2 - 10, H - 180 - offset * 2)
        offset -= 20
    step = 0
    draw_text(win, 'Game Over', W // 2, H - 450)
    draw_text(win, f'Ввш результать: {score}', W // 2, H // 2)
    draw_text(win, 'Best scores:', W // 2, H - 250)
    pg.display.flip()
