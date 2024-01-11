import pygame
import sqlite3
import random

pygame.init()
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
nq = True
answer = ''
right_an = ''
primer = ''
go_an = 0
ba_an = 0

class Button:
    def __init__(self):
        pass

    def button_create(self, text, rect, inactive_color, active_color, action):
        font = pygame.font.Font(None, 30)
        button_rect = pygame.Rect(rect)
        text = font.render(text, True, WHITE)
        text_rect = text.get_rect(center=button_rect.center)
        return [text, text_rect, button_rect, inactive_color, active_color, action, False]

    def button_check(self, info, event):
        text, text_rect, rect, inactive_color, active_color, action, hover = info
        if event.type == pygame.MOUSEMOTION:
            info[-1] = rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if hover and action:
                action()

    def button_draw(self, screen, info):
        text, text_rect, rect, inactive_color, active_color, action, hover = info
        if hover:
            color = active_color
        else:
            color = inactive_color
        pygame.draw.rect(screen, color, rect)
        screen.blit(text, text_rect)


def on_click_button_game():
    global stage
    stage = 'game'


def on_click_button_shop():
    global stage
    stage = 'shop'

def on_click_button_next():
    global stage, nq
    nq = True
    stage = 'game'

def on_click_button_buy_cup():
    global cup, money
    if money >= 3:
        cup = 1
        money = money - 3
        save()

def on_click_button_exit():
    global stage
    global running
    stage = 'exit'
    running = False

def on_click_button_job():
    global answer, right_an, go_an, ba_an, stage
    if len(answer) != 0:
        if int(answer) == right_an:
            go_an += 1
            stage = 'good'
        else:
            ba_an += 1
            stage = 'bad'
    else:
        ba_an += 1
        stage = 'bad'
    answer = ''

def quest():
    global answer, right_an, nq, primer
    func = ['+', '-', '*', ':']
    elem = random.choice(func)
    x = random.randint(0, 999)
    if elem == '+':
        y = random.randint(0, 999 - x)
        right_an = x + y
    elif elem == '-':
        y = random.randint(0, x)
        right_an = x - y
    elif elem == '*':
        y = random.randint(0, 1000//x - 1)
        right_an = x * y
    else:
        deliteli = []
        for i in range(1, int(x ** 0.5)):
            if x % i == 0:
                deliteli.append(i)
        y = random.choice(deliteli)
        right_an = x // y
    nq = False
    primer = f'{x}{elem}{y}='

def on_click_button_return():
    global stage
    stage = 'menu'

def vvod(event):
    global answer, screen, BLUE
    okno_vvoda = pygame.Rect(450, 175, 75, 50)
    pygame.draw.rect(screen, BLUE, okno_vvoda)
    press = False
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_BACKSPACE:
            answer = answer[:-1]
        else:
            if len(answer) < 3:
                if event.unicode in '1234567890':
                    answer += event.unicode



def choice():
    con = sqlite3.connect("Game.db")
    cur = con.cursor()
    result = cur.execute(f"""SELECT * FROM info
                                WHERE id = 1""").fetchall()
    result = result[0]
    cup = int(result[1])
    money = int(result[2])
    day = int(result[3])
    con.close()
    return cup, money, day


def save():
    con = sqlite3.connect("Game.db")
    cur = con.cursor()
    sqlite_insert_query = f"""UPDATE info 
                                SET cup = '{cup}', money = '{money}'
                                WHERE id = '{1}'"""
    cur.execute(sqlite_insert_query)
    con.commit()
    con.close()



cup, money, day = choice()
stat_font = pygame.font.Font(None, 35)
font_x = pygame.font.Font(None, 30)
font = pygame.font.Font(None, 60)
text_money = stat_font.render(f"Деньги: {money}", True, "#FF8000", "#FFEFD5")
money_pos = text_money.get_rect(center=(60, 15))
go_an_text = stat_font.render(f"Правильных ответов: {go_an} из 10", True, GREEN, "#FFEFD5")
go_an_text_pos = text_money.get_rect(center=(60, 15))
ba_an_text = stat_font.render(f"Неправильных ответов: {ba_an} из 5", True, RED, "#FFEFD5")
ba_an_text_pos = text_money.get_rect(center=(490, 15))
cup_text = font_x.render(f"Цена: 3", True, RED, BLUE)
cup_text_pos = cup_text.get_rect(center=(400, 135))
btn = Button()
pygame.init()
screen = pygame.display.set_mode((800, 600))
screen_rect = screen.get_rect()

stage = 'menu'

button_1 = btn.button_create("Старт", (350, 140, 100, 50), RED, GREEN, on_click_button_game)
button_2 = btn.button_create("Магазин", (350, 200, 100, 50), RED, GREEN, on_click_button_shop)
button_3 = btn.button_create("Выход", (350, 260, 100, 50), RED, GREEN, on_click_button_exit)
btn_job = btn.button_create("Подтвердить", (225, 280, 350, 45), GREEN, BLACK, on_click_button_job)
btn_next = btn.button_create("Следующий пример", (225, 280, 350, 45), GREEN, BLACK, on_click_button_next)
btn_cup = btn.button_create("Купить", (300, 270, 200, 40), RED, BLACK, on_click_button_buy_cup)
button_return = btn.button_create("X", (550, 125, 25, 25), RED, 'DarkRed', on_click_button_return)
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if stage == 'menu':
            btn.button_check(button_1, event)
            btn.button_check(button_2, event)
            btn.button_check(button_3, event)
        elif stage == 'game':
            btn.button_check(button_return, event)
            vvod(event)
            if nq:
                quest()
            btn.button_check(btn_job, event)
            go_an_text = stat_font.render(f"Правильных ответов: {go_an} из 10", True, GREEN, "#FFEFD5")
            ba_an_text = stat_font.render(f"Неправильных ответов: {ba_an} из 5", True, RED, "#FFEFD5")
            if go_an == 10:
                go_an = 0
                ba_an = 0
                stage = 'menu'
                money += 1
                text_money = stat_font.render(f"Деньги: {money}", True, "#FF8000", "#FFEFD5")
                save()
            if ba_an == 5:
                go_an = 0
                ba_an = 0
                stage = 'menu'
                save()
        elif stage == 'bad' or stage == 'good':
            btn.button_check(btn_next, event)
            btn.button_check(button_return, event)
        elif stage == 'shop':
            btn.button_check(btn_cup, event)
            btn.button_check(button_return, event)
            text_money = stat_font.render(f"Деньги: {money}", True, "#FF8000", "#FFEFD5")

    screen.fill(BLACK)
    wall = pygame.draw.rect(screen, '#FFEFD5', (0, 0, 800, 400), 0)
    table = pygame.draw.rect(screen, '#8B4513', (0, 400, 800, 400), 0)
    monitor = pygame.draw.rect(screen, 'gray', (200, 100, 400, 250), 0)
    pc_table = pygame.draw.rect(screen, 'blue', (225, 125, 350, 200), 0)
    pc_leg_1 = pygame.draw.rect(screen, 'gray', (350, 350, 100, 25), 0)
    pc_leg_2 = pygame.draw.polygon(screen, 'gray', [(250, 400), (550, 400), (400, 350)], 0)
    if stage == 'menu':
        btn.button_draw(screen, button_1)
        btn.button_draw(screen, button_2)
        btn.button_draw(screen, button_3)
        screen.blit(text_money, money_pos)
    elif stage == 'game':
        btn.button_draw(screen, btn_job)
        screen.blit(font.render(primer, True, BLACK), (250, 180, 75, 50))
        screen.blit(go_an_text, go_an_text_pos)
        screen.blit(ba_an_text, ba_an_text_pos)
        screen.blit(font.render(answer, True, BLACK), (450, 180, 75, 50))
        btn.button_draw(screen, button_return)
    elif stage == 'good':
        font_y = pygame.font.Font(None, 30)
        screen.blit(font_y.render("Правильный ответ!", True, GREEN), (250, 180, 75, 50))
        btn.button_draw(screen, btn_next)
        btn.button_draw(screen, button_return)
    elif stage == 'bad':
        screen.blit(font_x.render(f"Неправильный ответ!", True, RED), (250, 180, 75, 50))
        screen.blit(font_x.render(f"Правильный ответ {right_an}", True, RED), (250, 230, 75, 50))
        btn.button_draw(screen, btn_next)
        btn.button_draw(screen, button_return)
    elif stage == 'shop':
        screen.blit(text_money, money_pos)
        buy_rect = pygame.draw.rect(screen, '#CC00CC', (300, 325 - 175, 200, 150), 0)
        btn.button_draw(screen, btn_cup)
        cuple = pygame.draw.rect(screen, 'SteelBlue', (700-325, 325-150, 50, 75), 0)
        cuple_hand = pygame.draw.rect(screen, 'SteelBlue', (675-325, 335-150, 25, 40), 0)
        cuple_void = pygame.draw.rect(screen, '#CC00CC', (680-325, 340-150, 20, 30), 0)
        screen.blit(cup_text, cup_text_pos)
        btn.button_draw(screen, button_return)
    elif stage == 'shop':
        btn.button_draw(screen, button_return)
    if cup == 1:
        cuple = pygame.draw.rect(screen, 'SteelBlue', (700, 325, 50, 75), 0)
        cuple_hand = pygame.draw.rect(screen, 'SteelBlue', (675, 335, 25, 40), 0)
        cuple_void = pygame.draw.rect(screen, '#FFEFD5', (680, 340, 20, 30), 0)
    pygame.display.update()

pygame.quit()
