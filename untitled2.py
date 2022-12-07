import pygame
import math
from math import atan2, degrees, radians
import random
import time

def updatebullets():
    for i in bullets:
        if i[4] < 80: 
            i[0] += i[2]
            i[1] += i[3]
            i[4] += 1
            if i[0] > xsize:
                i[0] = i[0] - xsize
                i[4] += xsize/edgepenetration
            if i[1] > ysize:
                i[1] = i[1] - ysize
                i[4] += ysize/edgepenetration
            if i[0] < 0:
                i[0] = xsize - i[0]
                i[4] += xsize/edgepenetration
            if i[1] < 0:
                i[1] = ysize - i[1]
                i[4] += ysize/edgepenetration
            pygame.draw.circle(win, (255,255,255), (i[0], i[1]), 5.0, width=0)

        else:
            bullets.remove(i)


def updateasts():
    for i in l_ast:
        i[0] += i[2]
        i[1] += i[3]
        if i[0] > xsize:
            i[0] = i[0] - xsize
        if i[1] > ysize:
            i[1] = i[1] - ysize
        if i[0] < 0:
            i[0] = xsize - i[0]
        if i[1] < 0:
            i[1] = ysize - i[1]
        draw_ast(i[0], i[1], i[4])

    for i in m_ast:
        i[0] += i[2]
        i[1] += i[3]
        if i[0] > xsize:
            i[0] = i[0] - xsize
        if i[1] > ysize:
            i[1] = i[1] - ysize
        if i[0] < 0:
            i[0] = xsize - i[0]
        if i[1] < 0:
            i[1] = ysize - i[1]
        draw_ast(i[0], i[1], i[4])

    for i in s_ast:
        i[0] += i[2]
        i[1] += i[3]
        if i[0] > xsize:
            i[0] = i[0] - xsize
        if i[1] > ysize:
            i[1] = i[1] - ysize
        if i[0] < 0:
            i[0] = xsize - i[0]
        if i[1] < 0:
            i[1] = ysize - i[1]
        draw_ast(i[0], i[1], i[4])
    

def spawn_asts(level):
    for i in range(int((level+1)/2)+4):
        ypos = random.randint(0,ysize)
        if bool(random.getrandbits(1)):
            xpos = random.randint(0, int((xsize/4)))
        else:
            xpos = random.randint(int((xsize/2*1.5)), xsize)

        yspd = (random.randint(int(ast_speedlimit*10/5),int(ast_speedlimit/2*10)))/10
        xspd = (random.randint(0, int(ast_speedlimit*10/9)))/10

        if bool(random.getrandbits(1)):
            yspd = -yspd
        if bool(random.getrandbits(1)):
            xspd = -xspd

        l_ast.append([xpos, ypos, xspd, yspd, gerar_ast('L')])


def spawn_asts_v2(x, y, s):
    if s == 'L':
        for i in range (2):
            yspd = (random.randint(0,int(ast_speedlimit*0.7*10)))/10
            xspd = (random.randint(0, int(ast_speedlimit*0.5*10)))/10

            if bool(random.getrandbits(1)):
                yspd = -yspd
            if bool(random.getrandbits(1)):
                xspd = -xspd

            m_ast.append([x, y, xspd, yspd, gerar_ast('M')])

    elif s == 'M':
        for i in range (2):
            yspd = (random.randint(0,int(ast_speedlimit*10)))/10
            xspd = (random.randint(0, int(ast_speedlimit*0.7*10)))/10

            if bool(random.getrandbits(1)):
                yspd = -yspd
            if bool(random.getrandbits(1)):
                xspd = -xspd
            
            s_ast.append([x, y, xspd, yspd, gerar_ast('S')])


def gerar_ast(s):
    if s == 'L':
        coordenadas = []
        for k in range(8):
            for i in range(1):
                alphas = [random.uniform(0, 45), random.uniform(45, 90), random.uniform(90, 135), random.uniform(135, 180), random.uniform(180, 225), random.uniform(225, 270), random.uniform(270, 315), random.uniform(315, 360)]
                d = random.uniform(l_size*0.9, l_size*1.1)
                i = d * math.cos(math.radians(alphas[k]))
                j = d * math.sin(math.radians(alphas[k]))
                coordenadas.append((i, j))
        return coordenadas

    elif s == 'M':
        coordenadas = []
        for k in range(8):
            for i in range(1):
                alphas = [random.uniform(0, 45), random.uniform(45, 90), random.uniform(90, 135), random.uniform(135, 180), random.uniform(180, 225), random.uniform(225, 270), random.uniform(270, 315), random.uniform(315, 360)]
                d = random.uniform(m_size*0.9, m_size*1.1)
                i = d * math.cos(math.radians(alphas[k]))
                j = d * math.sin(math.radians(alphas[k]))
                coordenadas.append((i, j))
        return coordenadas

    elif s == 'S':
        coordenadas = []
        for k in range(8):
            for i in range(1):
                alphas = [random.uniform(0, 45), random.uniform(45, 90), random.uniform(90, 135), random.uniform(135, 180), random.uniform(180, 225), random.uniform(225, 270), random.uniform(270, 315), random.uniform(315, 360)]
                d = random.uniform(s_size*0.9, s_size*1.1)
                i = d * math.cos(math.radians(alphas[k]))
                j = d * math.sin(math.radians(alphas[k]))
                coordenadas.append((i, j))
        return coordenadas


def draw_ast(x, y, s):
    pos_ast = []
    for i in s:
        pos_ast.append(((i[0]+x),(i[1]+y)))

    pygame.draw.polygon(win, (255,255,255), pos_ast, width=2)


def ship_collision(ship_x, ship_y):
    global enemy_y, enemy_x, score, enemy_spawn

    for i in l_ast:
        dist = abs((((i[0] - ship_x)**2) + ((i[1] - ship_y)**2))**(1/2))
        if dist < l_size*1.15:
            spawn_asts_v2(i[0], i[1], 'L')
            l_ast.remove(i)
            collide()
    for i in m_ast:
        dist = abs((((i[0] - ship_x)**2) + ((i[1] - ship_y)**2))**(1/2))
        if dist < m_size*1.15:
            spawn_asts_v2(i[0], i[1], 'M')
            m_ast.remove(i)
            collide()  
    for i in s_ast:
        dist = abs((((i[0] - ship_x)**2) + ((i[1] - ship_y)**2))**(1/2))
        if dist < s_size*1.15:
            s_ast.remove(i)
            collide()

    dist = abs((((enemy_x - ship_x)**2) + ((enemy_y - ship_y)**2))**(1/2))
    if dist < radius*1.1 and enemy_spawn == 1:
        enemy_spawn = 0
        score -= 500
    
        collide()

def collide():
    global lives, ticker, x, y, xvel, yvel, angle, enemy_spawn
    enemy_spawn = 0
    lives -= 1
    ticker = 180
    x = xsize/2
    y = ysize/2
    xvel, yvel = 0,0
    angle = 180


def bullet_collision():
    global score, enemy_spawn, enemy_x, enemy_y, ticker
    for bullet in bullets:
        for ast in l_ast:
            dist = abs((((ast[0] - bullet[0])**2) + ((ast[1] - bullet[1])**2))**(1/2))
            if dist < l_size:
                spawn_asts_v2(ast[0], ast[1], 'L')
                l_ast.remove(ast)
                score += 50
                try:
                    bullets.remove(bullet)
                except:
                    pass

        for ast in m_ast:
            dist = abs((((ast[0] - bullet[0])**2) + ((ast[1] - bullet[1])**2))**(1/2))
            if dist < m_size:
                spawn_asts_v2(ast[0], ast[1], 'M')
                m_ast.remove(ast)
                score += 100
                try:
                    bullets.remove(bullet)
                except:
                    pass

        for ast in s_ast:
            dist = abs((((ast[0] - bullet[0])**2) + ((ast[1] - bullet[1])**2))**(1/2))
            if dist < s_size:
                s_ast.remove(ast)
                score += 150
                try:
                    bullets.remove(bullet)
                except:
                    pass

        dist = abs((((x - bullet[0])**2) + ((y - bullet[1])**2))**(1/2))
        if (dist < radius) and bullet[5] == 1:
            score -= 500
            try:
                bullets.remove(bullet)
            except:
                pass
            if ticker == 0:
                collide()

        dist = abs((((enemy_x - bullet[0])**2) + ((enemy_y - bullet[1])**2))**(1/2))
        if (dist < radius*1.1) and bullet[5] == 0:
            score += 500
            try:
                bullets.remove(bullet)
            except:
                pass
            enemy_spawn = 0


def leveluptest(): 
    if (len(l_ast) == 0) and (len(m_ast) == 0) and (len(s_ast) == 0):
        global  level, start, secs
        level += 1
        start = 1
        enemy_spawn = 1
        secs = 0


def draw_ship():
    hist.append([x,y])
    if len(hist) > 100:
        hist.pop(0)
    anglep2 = angle + 135
    anglep3 = angle + 135 + 90
    
    if anglep2 >= 360:
        anglep2 -= 360
        
    if anglep3 >= 360:
        anglep3 -= 360

    point1 = (((math.sin(math.radians(angle)))*radius)+x,((math.cos(math.radians(angle)))*radius)+y)
    point2 = (((math.sin(math.radians(anglep2)))*radius)+x,((math.cos(math.radians(anglep2)))*radius)+y)
    point3 = (((math.sin(math.radians(anglep3)))*radius)+x,((math.cos(math.radians(anglep3)))*radius)+y)
    pos = [point1, point2, point3]
    
    midfire = (((math.sin(math.radians(angle)))*(radius-40))+x,((math.cos(math.radians(angle)))*(radius-40))+y)
    pointfire = (((math.sin(math.radians(angle)))*(radius-30))+x,((math.cos(math.radians(angle)))*(radius-30))+y)

    pygame.draw.polygon(win, (0,255,0), pos, width= 2)

    if keys[pygame.K_UP]:
        pygame.draw.line(win, (255,127,0), midfire, pointfire, width=5)


def enemy_logic():
    global enemy_x, enemy_y, global_pulse

    if len(hist) > 99:
        enemy_x = (hist[0])[0]
        enemy_y = (hist[0])[1]

    enemy_color = (255,0,0)
    enemy_vertices = [(0,0), (-15,25), (15,25), (20,15), (-20,15), (0,10), (10,20), (-10,20), (0,20), (-10,5), (0,5)]
    enemy_pos = []
    arc_pos = []

    for i in enemy_vertices:
        enemy_pos.append((i[0]+enemy_x, i[1]+enemy_y))

    for i in enemy_pos[9]:
        arc_pos.append(i)
    
    arc_pos.append(20)
    arc_pos.append(20)

    if global_pulse == 1 and secs%2 == 0:
        enemy_attack([enemy_x, enemy_y])

    pygame.draw.polygon(win, enemy_color, enemy_pos[1:5], width= 2)
    pygame.draw.circle(win, enemy_color, enemy_pos[6], 1, width= 2)
    pygame.draw.circle(win, enemy_color, enemy_pos[7], 1, width= 2)
    pygame.draw.circle(win, enemy_color, enemy_pos[8], 1, width= 2)
    pygame.draw.arc(win, enemy_color, (arc_pos), 0, math.pi, 2)
    pygame.draw.line(win, enemy_color, enemy_pos[0], enemy_pos[10], width= 2)
    return([enemy_x, enemy_y])
    

def enemy_attack(pos):
    angle_en = angulo_enemy(pos)

    incx = ((math.sin(math.radians(angle_en)))*bltspd*0.7)
    incy = ((math.cos(math.radians(angle_en)))*bltspd*0.7)
    bullets.append([pos[0], pos[1], incx, incy, 0, 1])



def teleport():
    return [(random.randint(0,xsize)), (random.randint(0,ysize))]



def angulo_enemy(pos):
    global x,y

    point_1 = [x,y]
    point_2 = pos

    angulinho = atan2(point_2[1] - point_1[1], point_2[0] - point_1[0])

    angulinho = (angulinho/math.pi) * 180

    if angulinho < 0:
        angulinho = 360 + angulinho

    angulinho = (360-angulinho) - 90

    if angulinho < 0:
        angulinho = 360 + angulinho

    print(angulinho)
    return angulinho


pygame.init()

xsize = 900
ysize = 900

win = pygame.display.set_mode((xsize,ysize))

pygame.display.set_caption("Asteroids")

x = xsize/2
y = ysize/2
enemy_x = xsize/1.75
enemy_y = ysize/1.75
enemy_x_spd = 0
enemy_y_spd = 0
radius = ysize/60
angle = 180
rotspd = 120
xvel = 0
yvel = 0  
accel = 3
speedlimit = 15
enemyspd = 7
decell = 7
bltspd = 20
edgepenetration = 18
start = 1 
ast_speedlimit = 6
score = 0
l_size = ysize/18
m_size = ysize/30
s_size = ysize/60
lives = 3
ticker = 0
ticks = 0
secs = 0
global_pulse = 0

fonte = pygame.freetype.Font("fonte.ttf", 100)
livesf = pygame.freetype.Font("fonte.ttf", 50)

s_ast = []
m_ast = []
l_ast = []

hist = []

level = 0

enemy_spawn = 0

bullets = []

run = True
while run:

    if (level >=1) and (secs == 10):
        enemy_spawn = 1
    if (level >=3) and (math.floor(secs/13)%2==0) and (math.floor(secs/13)*13 == secs) and (math.floor(secs/13) != 0):
        enemy_spawn = 1

    if ticks == 60:
        secs += 1
        ticks = 0
        global_pulse = 1
    else:
        ticks += 1
        global_pulse = 0

    pygame.time.delay(16)

    win.fill((0,0,0))
    fonte.render_to(win, (50, 50), str(score) , (255, 255, 255))
    livesf.render_to(win, (55, 100), str(lives) , (255, 255, 255))

    if ticker != 0:
        ticker -= 1

    if start == 1:
        if enemy_spawn == 1:
            pass
        x = xsize/2
        y = ysize/2
        xvel = 0
        yvel = 0
        spawn_asts(level)
        start = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            break

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and ticker < 120:
                incx = ((math.sin(math.radians(angle)))*bltspd)
                incy = ((math.cos(math.radians(angle)))*bltspd)
                bullets.append([x, y, incx, incy, 0, 0])

            if event.key == pygame.K_DOWN:
                newpos = teleport()
                ticker = 60
                x = newpos[0]
                y = newpos[1]

    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_LEFT]:
        angle += rotspd/20
        
    if keys[pygame.K_RIGHT]:
        angle -= rotspd/20
    
    if keys[pygame.K_UP]:
        if ticker < 120:
            if abs(yvel) < speedlimit:
                yvel += (math.cos(math.radians(angle)))*accel/20
            elif yvel > 0 and (math.cos(math.radians(angle)))*accel/20 < 0:
                yvel += (math.cos(math.radians(angle)))*accel/20
            elif yvel < 0 and (math.cos(math.radians(angle)))*accel/20 > 0:
                yvel += (math.cos(math.radians(angle)))*accel/20
            
            if abs(xvel) < speedlimit:
                xvel += (math.sin(math.radians(angle)))*accel/20
            elif xvel > 0 and (math.sin(math.radians(angle)))*accel/20 < 0:
                xvel += (math.sin(math.radians(angle)))*accel/20
            elif xvel < 0 and (math.sin(math.radians(angle)))*accel/20 > 0:
                xvel += (math.sin(math.radians(angle)))*accel/20

    else:
        yvel = yvel/(1+(decell/1000))
        xvel = xvel/(1+(decell/1000))
    
    if angle < 0:
        angle += 360
    elif angle >= 360:
        angle -= 360
        
    x = x + xvel
    y = y + yvel

    if x > xsize:
        x = x - xsize
    if y > ysize:
        y = y - ysize
    if x < 0:
        x = xsize - x
    if y < 0:
        y = ysize - y

    if not run:
        break

    if ticker < 120:
        rounded = math.floor(ticker/10)
        if rounded % 2 == 0:
            draw_ship()
    
    if ticker == 0:
        ship_collision(x, y)
        bullet_collision()
        
    if enemy_spawn == 1:
        enemy_logic()

    updatebullets()  
    updateasts()
    leveluptest()
    
    pygame.display.update()
pygame.quit()