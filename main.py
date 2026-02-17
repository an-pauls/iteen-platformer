import pygame
from classes import *
from constructor import *

screen = pygame.display.set_mode([0, 0], pygame.FULLSCREEN)
clock = pygame.time.Clock()

score = 0
frame = 0
level = 0
maps = ['Dark Forest.txt',
        'map.txt',
        'Hisoka.txt',
        'Forest.txt',
  #      'jumper.txt',
        'dambs.txt',
        'abandoned_swamp.txt',
        'Всевидящий лес.txt',
        'Way to light.txt',
        'Void rush.txt',
        'mountains.txt',
        'DARK.SIDE.txt',
        'Gold_Bunny.txt'
       ]

# Создаём меню
menu = Menu(
    ['Игра', 'Конструктор', 'Выход'],
    'fonts/PF Stamps Pro Metal.ttf',
    'White',
    'DarkGray',
    'center'
)
interface = Interface()

# Создаём конструктор и карту
constructor = Constructor(mapSize=[48, 27])
map = Map(maps[level])

# Игрок
player = Hero(map.player_pos, 0.5, -12)

def handler():
    global map, player, level
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
        if event.type == pygame.MOUSEBUTTONDOWN and menu.mode == 'menu':
            for item in range(len(menu.items)):
                if menu.rects[item].collidepoint(pygame.mouse.get_pos()):
                    if menu.items[item] == 'Игра':
                        map = Map(maps[level])
                        player = Hero(map.player_pos, 0.5, -12)
                        menu.mode = 'game'
                    elif menu.items[item] == 'Конструктор':
                        menu.mode = 'constructor'
                    elif menu.items[item] == 'Выход':
                        quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                menu.mode = 'menu'
            if event.key == pygame.K_n:
                if level < len(maps)-1:
                    level += 1
                map = Map(maps[level])
                player = Hero(map.player_pos, 0.5, -12)
    # Управление персонажем
    keys = pygame.key.get_pressed()
    if keys[pygame.K_RIGHT]:
        player.dir = 'right'
        player.type = 'walk'
        player.rect.x += 4
    elif keys[pygame.K_LEFT]:
        player.dir = 'left'
        player.type = 'walk'
        player.rect.x -= 4
    elif keys[pygame.K_SPACE]:
        player.type = 'attack'
    else:
        player.type = 'idle'

    if keys[pygame.K_UP]:
        if player.move == 'stay':
            player.Vy = player.Vjump
            player.move = 'fall'

def collider():
    global score
    collide_dir = None
    for key in map.tiles:
        rect = map.tiles[key]['rect']
        if player.rect.colliderect(rect) and map.tiles[key]['type'] == 'tile':
            bottom = abs(player.rect.bottom - rect.top)
            top = abs(player.rect.top - rect.bottom)
            left = abs(player.rect.left - rect.right)
            right = abs(player.rect.right - rect.left)

            if min(bottom, top, left, right) == bottom and player.Vy > 0:
                collide_dir = 'down'
                player.rect.bottom = rect.top
            elif min(bottom, top, left, right) == top and player.Vy < 0:
                collide_dir = 'up'
            elif min(bottom, top, left, right) == left:
                collide_dir = 'left'
                player.rect.left = rect.right
            elif min(bottom, top, left, right) == right:
                collide_dir = 'right'
                player.rect.right = rect.left
            break

        elif player.rect.colliderect(rect) and map.tiles[key]['type'] == 'Coin':
            score += 1
            map.tiles.pop(key)
            break
        elif player.rect.colliderect(rect) and map.tiles[key]['type'] == 'Rune':
            score += 10
            map.tiles.pop(key)
            break
        elif player.rect.colliderect(rect) and map.tiles[key]['type'] == 'Rune':
            if player.key:
                level += 1
                map.__init__(maps[level])
                player.__init__(map.player_pos, 0.5, -12)
            break

    if collide_dir == 'down':
        player.move = 'stay'
        player.Vy = 0
    elif collide_dir == 'up':
        player.Vy *= -1
        player.move = 'fall'
    elif collide_dir == None:
        player.move = 'fall'

while True:
    handler()
    collider()
    screen.fill('Black')

    if menu.mode == 'constructor':
        constructor.draw(screen)
    elif menu.mode == 'game':
        frame += 1
        map.draw_background(screen)
        player.draw(screen)
        map.draw_tiles(screen)
        interface.draw(screen,maps[level][:-4],score,frame//60)
    elif menu.mode == 'menu':
        menu.draw(screen)

    clock.tick(60)
    pygame.display.update()