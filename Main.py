#                        
#　　　　　　　　　　_,.. -──- ､,
#　　　　　　　　,　'" 　 　　　 　　 `ヽ.
#　　　　　　 ／/¨7__　　/ 　 　 i　 _厂廴
#　　　　　 /￣( ノ__/　/{　　　　} ｢　（_冫}
#　　　　／￣l＿// 　/-|　 ,!　 ﾑ ￣|＿｢ ＼＿_
#　　. イ　 　 ,　 /!_∠_　|　/　/_⊥_,ﾉ ハ　 イ 
#　　　/ ／ / 　〃ん心 ﾚ'|／　ｆ,心 Y　i ＼_＿＞　
#　 ∠イ 　/　 　ﾄ弋_ツ　　 　 弋_ﾂ i　 |　 | ＼
#　 _／ _ノ|　,i　⊂⊃　　　'　　　⊂⊃ ./　 !､＿ン
#　　￣　　∨|　,小、　　` ‐ ' 　　 /|／|　/
#　 　 　 　 　 Y　|ﾍ＞ 、 ＿ ,.　イﾚ|　 ﾚ'
#　　　　　　 r'.| 　|;;;入ﾞ亠―亠' );;;;;! 　|､
#　　　　　 ,ノ:,:|.　!|く　__￣￣￣__У　ﾉ|:,:,ヽ
#　　　　　(:.:.:.:ﾑ人!ﾍ　 　` ´ 　　 厂|ノ:.:.:丿 by @RomSTil


import pygame
from random import randrange as rnd

pygame.init()

screen_width = 1100
screen_height = 800
fps = 60
#ракетка
racket_w = 350
racket_h = 35
racket_speed = 2
racket = pygame.Rect(screen_width // 2 - racket_w // 2, screen_height - racket_h - 10, racket_w, racket_h)


#мяч 
ball_radius = 20
ball_speed = 1
ball_rect = int(ball_radius * 2 ** 0.5)
ball = pygame.Rect(rnd(ball_rect, screen_width - ball_rect), screen_height // 2, ball_rect, ball_rect)
dx, dy = 1, -1
#кирпидончики
block_list = [pygame.Rect(10 + 111 * i, 10 + 70 * j, 100, 50) for i in range(10) for j in range(4)]
color_list = [(rnd(30, 256), rnd(30, 256), rnd(30, 256)) for i in range(10) for j in range(4)]


#создание окна и прописывание параметров для него 
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('By RomSTil')
Icon = pygame.image.load('Icon.png')
pygame.display.set_icon(Icon)

#цвета
color_white = (240,245,249)
color_black = (30,32,34)
color_gray = (201,214,223)

def detect_collision(dx, dy, ball, rect):
    if dx > 0:
        delta_x = ball.right - rect.left 
    else:
        delta_x =  rect.right - ball.left
    
    if  dy > 0:
        delta_y  = ball.bottom - rect.top
    else:
        delta_y = rect.bottom - ball.top

    if abs(delta_x - delta_y) < 10:
        dx, dy = -dx, -dy
    elif delta_x > delta_y:
        dy = -dy
    elif delta_y > delta_x:
        dx = -dx

    return dx, dy

run =  True
while run:
    #рисование бекграунда
    screen.fill(color_black)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    #создание ракетки, мячика, блоков
    [pygame.draw.rect(screen, color_list[color], block) for color, block  in enumerate(block_list)]
    pygame.draw.rect(screen, color_white, racket)
    pygame.draw.circle(screen, color_gray, ball.center, ball_radius)
    
    #полет меча 
    ball.x +=  ball_speed * dx 
    ball.y += ball_speed * dy
    #колизия стенок лево/право
    if ball.centerx < ball_radius or ball.centerx > screen_width - ball_radius:
        dx = -dx
    
    #колизия стенки сверху
    if ball.centery < ball_radius:
        dy = -dy

    #колизия рокетки
    if ball.colliderect(racket) and dy > 0:
        dx, dy = detect_collision(dx, dy, ball, racket)

    #колизия блоков 
    hit_index = ball.collidelist(block_list)
    if hit_index != -1:
        hit_rect = block_list.pop(hit_index)
        hit_color = color_list.pop(hit_index)
        dx, dy = detect_collision(dx, dy, ball, hit_rect)
    #управление ракетки
    key = pygame.key.get_pressed()
    if key[pygame.K_LEFT] and racket.left > 0:
        racket.left -= racket_speed
    if key[pygame.K_RIGHT] and racket.right < screen_width:
        racket.right += racket_speed


    #обновление экрана
    pygame.display.update()

pygame.quit()