import pygame
import random
pygame.init()
import os

class Map:
    def __init__(self):
        self.frame = 0
        self.tiles = {}
        self.background = None
        self.player_pos = []

        with open('maps/map.txt', 'r') as file:
            input = eval(file.read())

        tileset = None

        for key in input:
            if isinstance(input[key], list):
                imageInfo = input[key]
                x = imageInfo[1]*imageInfo[3]
                y = imageInfo[2]*imageInfo[3]
                size = imageInfo[3]
                if tileset == None:
                    tileset = pygame.image.load(imageInfo[0]).convert_alpha()
                tile = tileset.subsurface([x, y, size, size])
                sprite = pygame.transform.scale_by(tile, 1.25)

                pos = key.split('-')
                rect = pygame.Rect([int(pos[0]), int(pos[1]), 40, 40])

                self.tiles[key] = {'image': sprite, 'rect': rect, 'type': 'tile'}
            elif isinstance(input[key], str):
                if key == 'background':
                    path = input[key]
                    self.background = pygame.image.load(path).convert_alpha()
                elif 'Objects' in input[key]:
                    pos = key.split('-')
                    rect = pygame.Rect([int(pos[0]), int(pos[1]), 40, 40])
                    sprite = pygame.image.load(input[key]).convert_alpha()
                    sprite = pygame.transform.scale_by(sprite, 1.25)
                    final = pygame.Surface((40, 40), pygame.SRCALPHA)
                    x_pos = (40 - sprite.get_width()) // 2
                    y_pos = 40 - sprite.get_height()
                    final.blit(sprite, (x_pos, y_pos))
                    self.tiles[key] = {'image': final, 'rect': rect, 'type': 'object'}
                elif 'Animated objects' in input[key]:
                    sprites = []
                    img = pygame.image.load(input[key]).convert_alpha()
                    w = img.get_width() // 4
                    h = img.get_height()
                    for i in range(4):
                        sprite = img.subsurface([i * w, 0, w, h])
                        if sprite.get_width() < 32:
                            sprite = pygame.transform.scale_by(sprite, 1.7)
                        elif sprite.get_width() > 32:
                            sprite = pygame.transform.scale_by(sprite, 0.6)
                        sprite = pygame.transform.scale_by(sprite, 1.25)
                        final = pygame.Surface((40, 40), pygame.SRCALPHA)
                        x_pos = (40 - sprite.get_width()) // 2
                        y_pos = (40 - sprite.get_height()) // 2
                        final.blit(sprite, (x_pos, y_pos))
                        sprites.append(final)

                    pos = key.split('-')
                    rect = pygame.Rect([int(pos[0]), int(pos[1]), 40, 40])
                    self.tiles[key] = {'image': sprites, 'rect': rect, 'type': input[key].split('/')[-1][:-4]}
                elif 'Player' in input[key]:
                    pos = key.split('-')
                    self.player_pos = [int(pos[0]), int(pos[1])]

    def draw_background(self, screen):
        if self.background != None:
            screen.blit(self.background, [0, 0])

    def draw_tiles(self, screen):
        self.frame += 0.2
        for key in self.tiles:
            if isinstance(self.tiles[key]['image'], list):
                current = self.frame % 4
                screen.blit(self.tiles[key]['image'][int(current)], self.tiles[key]['rect'])
            else:
                screen.blit(self.tiles[key]['image'], self.tiles[key]['rect'])



class Menu:
    def __init__(self, items:list, font_path:str,
                 active_color:str, passive_color:str, pos:str):
        self.mode = 'menu'
        self.font = pygame.font.Font(font_path, 48)
        self.items = items
        self.active_color = active_color
        self.passive_color = passive_color
        self.pos = pos
        self.renders = {'active':[], 'passive':[]}
        for item in self.items:
            render = self.font.render(item, True, self.passive_color)
            self.renders['passive'].append(render)
            render = self.font.render(item, True, self.active_color)
            self.renders['active'].append(render)

        H = pygame.display.Info().current_h
        W = pygame.display.Info().current_w
        self.margin = 25
        Hm = 0
        for item in self.renders['passive']:
            Hm += item.get_height()
        Hm += self.margin * (len(self.items) - 1)
        Y0 = H//2 - Hm//2 + self.renders['passive'][0].get_height()//2

        self.rects = []
        for item in self.renders['passive']:
            if self.pos == 'center':
                self.rects.append(item.get_rect(center=[W//2, Y0]))
            elif self.pos == 'left':
                self.rects.append(item.get_rect(midleft=[W//7, Y0]))
            elif self.pos == 'right':
                self.rects.append(item.get_rect(midright=[W - W//7, Y0]))
            Y0 += item.get_height() + self.margin


    def draw(self, screen):
        for item in range(len(self.items)):
            if self.rects[item].collidepoint(pygame.mouse.get_pos()):
                screen.blit(self.renders['active'][item], self.rects[item])
            else:
                screen.blit(self.renders['passive'][item], self.rects[item])


class Hero:
    def __init__(self, pos, g, Vy):
        self.Vy = 0
        self.Vjump = Vy
        self.g = g
        self.move = 'stay'

        self.frame = 0
        self.dir = 'right'
        self.type = 'idle'
        self.image = pygame.image.load('images/0 Player/sprite.png')
        self.sprites = {
            'idle': {'right': [], 'left': []},
            'walk': {'right': [], 'left': []},
            'jump': {'right': [], 'left': []},
        }

        self.pos = {
            'idle': [24, 4],
            'walk': [48, 4],
            'jump': [0, 1],
        }

        for key in self.pos.keys():
            for i in range(self.pos[key][1]):
                sprite = self.image.subsurface([16*i,
                                                self.pos[key][0],
                                                16,
                                                24])
                sprite = pygame.transform.scale_by(sprite, 2.5)
                self.sprites[key]['right'].append(sprite)
                sprite = pygame.transform.flip(sprite, True, False)
                self.sprites[key]['left'].append(sprite)

        self.rect = self.sprites['idle']['left'][0].get_rect(center=pos)

    def draw(self, screen):
        self.frame += 0.1
        current = self.frame % len(self.sprites[self.type][self.dir])
        screen.blit(self.sprites[self.type][self.dir][int(current)], self.rect)

        if self.move == 'fall':
            self.Vy += self.g
            self.rect.y += self.Vy
