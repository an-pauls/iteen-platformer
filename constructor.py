import pygame
import os
import pickle

class Constructor:
    def __init__(self, mapSize:list):
        self.frame = 0
        self.cols = mapSize[0]
        self.rows = mapSize[1]

        # UI
        self.buttons = {
            'save': {'img': [], 'rect': None, 'state': 0},
            'clear': {'img': [], 'rect': None, 'state': 0},
        }

        self.buttons['save']['img'].append(pygame.image.load('images/5 Icons/save.png').convert_alpha())
        self.buttons['save']['img'].append(pygame.image.load('images/5 Icons/save_ok.png').convert_alpha())
        self.buttons['clear']['img'].append(pygame.image.load('images/5 Icons/clear.png').convert_alpha())
        self.buttons['clear']['img'].append(pygame.image.load('images/5 Icons/clear_ok.png').convert_alpha())
        self.buttons['save']['rect'] = self.buttons['save']['img'][0].get_rect(topleft=[1675, 997])
        self.buttons['clear']['rect'] = self.buttons['save']['img'][0].get_rect(topleft=[1675, 951])

        # Пустая карта
        self.map = {}

        maps = os.listdir('maps')
        if 'draft_map.pkl' in maps:
            with open("maps/draft_map.pkl", "rb") as f:
                loaded_raw = pickle.load(f)
                self.map = self.unpack_data(loaded_raw)

        # Пустое превью
        self.preview = {}

        # Пустой фон
        self.background = {}

        # Пустая сетка карты
        self.emptyGrid()

        # Фоны
        self.load_backgrounds()

        # Палитра тайлов
        self.tilesPallete(x0=(self.cols+2))

        # Палитра объектов
        self.objectsPallete()

        # Палитра анимированных спрайтов
        self.animatedObjectsPallete()

        # Палитра скина игрока
        self.playerPallete()

        if 'background' in self.map:
            back_name = self.map['background']['info'].split('/')[-1]
            index = os.listdir('images/2 Background').index(back_name)
            if self.back_names[index] != 'empty.png':
                image = pygame.transform.scale_by(self.back_images[index], 0.8)
                path = f'images/2 Background/{self.back_names[index]}'
                rect = self.back_preview_rects[index]
                self.background = {'image': image, 'rect': rect, 'info': path}

    def tilesPallete(self, tileSize = 32, x0 = 32):
        path = 'images/1 Tiles/Tileset.png'
        self.x0 = x0*tileSize - tileSize//2
        self.y0 = tileSize
        tileset = pygame.image.load(path).convert_alpha()
        cols = tileset.get_width()//tileSize
        rows = tileset.get_height()//tileSize

        self.tilesImages = []
        self.tilesInfo = []
        self.tilesPalleteRects = []
        for row in range(rows):
            for col in range(cols):
                tile = tileset.subsurface([col*tileSize, row*tileSize, tileSize, tileSize])
                self.tilesImages.append(tile)
                rect = pygame.Rect([self.x0 + col*tileSize, self.y0 + row*tileSize, tileSize, tileSize])
                self.tilesPalleteRects.append(rect)
                self.tilesInfo.append([path, col, row, 32])

    def emptyGrid(self, gridSize = 32):
        self.margin = 32
        self.gridSize = gridSize
        self.gridRects = []
        for row in range(self.rows):
            for col in range(self.cols):
                self.gridRects.append(pygame.Rect([self.margin + col*self.gridSize,
                                                   self.margin + row*self.gridSize,
                                                   self.gridSize,
                                                   self.gridSize]))
        self.gridBack = pygame.Rect([self.margin, self.margin, self.gridSize*self.cols, self.gridSize*self.rows])

    def load_backgrounds(self, path = 'images/2 Background'):
        x0 = 32
        y0 = 32*29
        self.back_images = []
        self.back_names = os.listdir(path)
        for item in self.back_names:
            self.back_images.append(pygame.image.load(f'{path}/{item}').convert_alpha())

        self.back_preview = []
        self.back_preview_rects = []
        for i in range(len(self.back_names)):
            if self.back_names[i] != 'empty.png':
                self.back_preview.append(pygame.transform.scale(self.back_images[i], [228, 128]))
                self.back_preview_rects.append(pygame.Rect([x0, y0, 228, 128]))
                x0 += 242
            else:
                self.back_preview.append(self.back_images[i])
                self.back_preview_rects.append(pygame.Rect([x0+16, y0+32, 83, 128]))

    def objectsPallete(self, path = 'images/3 Objects', tileSize = 32, x0 = 50):
        self.objectsImages = []
        self.objectsRects = []
        self.objectsInfo = []

        self.obj_dirs = os.listdir(path)
        self.x0 = x0 * tileSize - tileSize // 2
        self.y0 = tileSize * 8

        x = self.x0
        y = self.y0
        for dir in self.obj_dirs:
            files = os.listdir(f'{path}/{dir}')
            for image in files:
                sprite = pygame.image.load(f'{path}/{dir}/{image}').convert_alpha()
                final = pygame.Surface((tileSize , tileSize ), pygame.SRCALPHA)
                x_pos = (32 - sprite.get_width()) // 2
                y_pos = 32 - sprite.get_height()
                final.blit(sprite, (x_pos, y_pos))

                self.objectsRects.append(final.get_rect(topleft=[x, y]))
                self.objectsImages.append(final)
                self.objectsInfo.append(f'{path}/{dir}/{image}')
                x += 32
                if x > 1900:
                    x = self.x0
                    y += 32

    def animatedObjectsPallete(self, path = 'images/4 Animated objects', tileSize = 32, x0 = 50):
        self.animatedObjectsSprites = []
        self.animatedObjectsRects = []
        self.animatedObjectsInfo = []

        self.obj_dirs = os.listdir(path)
        self.x0 = x0 * tileSize - tileSize // 2
        self.y0 = tileSize * 14

        x = self.x0
        y = self.y0
        files = os.listdir(path)
        for image in files:
            sprites = []
            img = pygame.image.load(f'{path}/{image}').convert_alpha()
            w = img.get_width()//4
            h = img.get_height()

            for i in range(4):
                sprite = img.subsurface([i*w, 0, w, h])
                if sprite.get_width() < 32:
                    sprite = pygame.transform.scale_by(sprite, 1.7)
                elif sprite.get_width() > 32:
                    sprite = pygame.transform.scale_by(sprite, 0.6)
                final = pygame.Surface((tileSize, tileSize), pygame.SRCALPHA)
                x_pos = (tileSize - sprite.get_width()) // 2
                y_pos = (tileSize - sprite.get_height()) // 2
                final.blit(sprite, (x_pos, y_pos))
                sprites.append(final)

            self.animatedObjectsRects.append(sprites[0].get_rect(topleft=[x, y]))
            self.animatedObjectsSprites.append(sprites)
            self.animatedObjectsInfo.append(f'{path}/{image}')
            x += 42
            if x > 1900:
                x = self.x0
                y += 32

    def playerPallete(self, path = 'images/0 Player/sprite.png', tileSize = 32, x0 = 50):
        self.playerSprites = []
        self.playerRect = []
        self.playerInfo = []

        self.x0 = x0 * tileSize - tileSize // 2
        self.y0 = tileSize * 16

        sprites = []
        img = pygame.image.load(path).convert_alpha()
        w = img.get_width()//4
        h = img.get_height()//3

        for i in range(4):
            sprite = img.subsurface([i*w, h, w, h])
            sprite = pygame.transform.scale_by(sprite, 2)

            final = pygame.Surface((tileSize, tileSize), pygame.SRCALPHA)
            x_pos = (tileSize - sprite.get_width()) // 2
            y_pos = tileSize - sprite.get_height()
            final.blit(sprite, (x_pos, y_pos))
            sprites.append(final)

        self.animatedObjectsRects.append(sprites[0].get_rect(topleft=[self.x0, self.y0]))
        self.animatedObjectsSprites.append(sprites)
        self.animatedObjectsInfo.append(path)

    def back_click(self):
        for rect in self.back_preview_rects:
            if rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
                index = self.back_preview_rects.index(rect)
                if self.back_names[index] != 'empty.png':
                    image = pygame.transform.scale_by(self.back_images[index], 0.8)
                    path = f'images/2 Background/{self.back_names[index]}'
                    self.map['background'] = {'image': image, 'rect': rect, 'info': path }
                else:
                    if 'background' in self.map:
                        self.map.pop('background')

    def pallete_click(self, screen):
        if pygame.mouse.get_pressed()[0]:
            for item in self.tilesPalleteRects:
                if item.collidepoint(pygame.mouse.get_pos()):
                    index = self.tilesPalleteRects.index(item)
                    image = self.tilesImages[index]
                    info = self.tilesInfo[index]
                    self.preview = {'image': image, 'info': info, 'rect': item}
            for item in self.objectsRects:
                if item.collidepoint(pygame.mouse.get_pos()):
                    index = self.objectsRects.index(item)
                    image = self.objectsImages[index]
                    info = self.objectsInfo[index]
                    self.preview = {'image': image, 'info': info, 'rect': item}
            for item in self.animatedObjectsRects:
                if item.collidepoint(pygame.mouse.get_pos()):
                    index = self.animatedObjectsRects.index(item)
                    image = self.animatedObjectsSprites[index]
                    info = self.animatedObjectsInfo[index]
                    self.preview = {'image': image, 'info': info, 'rect': item}

        elif pygame.mouse.get_pressed()[2]:
            self.preview = {}

        if self.preview != {}:
            if isinstance(self.preview['image'], list):
                screen.blit(self.preview['image'][0], self.preview['rect'])
                self.preview['rect'] = self.preview['image'][0].get_rect(center=pygame.mouse.get_pos())
            else:
                screen.blit(self.preview['image'], self.preview['rect'])
                self.preview['rect'] = self.preview['image'].get_rect(center=pygame.mouse.get_pos())

    def grid_click(self):
        for item in self.gridRects:
            if item.collidepoint(pygame.mouse.get_pos()):

                if self.preview != {}:
                    self.preview['rect'] = item

                if pygame.mouse.get_pressed()[0]:
                    if self.preview != {}:
                        pos = f'{item.x}-{item.y}'
                        self.map[pos] = {'image': self.preview['image'], 'rect': item, 'info': self.preview['info']}
                        self.buttons['save']['state'] = 0
                        self.buttons['clear']['state'] = 0

                if pygame.mouse.get_pressed()[2]:
                    pos = f'{item.x}-{item.y}'
                    if pos in self.map:
                        self.map.pop(pos)
                    self.buttons['save']['state'] = 0

    def save(self):
        output = {}
        for key in self.map:
            if key != 'background':
                pos = key.split('-')
                x = int((int(pos[0])-32) * 1.25)
                y = int((int(pos[1])-32) * 1.25)
                output[f'{x}-{y}'] = self.map[key]['info']
            if key == 'background':
                output['background'] = self.map[key]['info']
        with open('maps/map.txt', 'w') as file:
            file.write(str(output))

        # Сериализация и сохранение карты редактора
        with open("maps/draft_map.pkl", "wb") as f:
            pickle.dump(self.pack_data(self.map), f)

    def pack_data(self, data):
        if isinstance(data, dict):
            return {k: self.pack_data(v) for k, v in data.items()}
        elif isinstance(data, list):
            return [self.pack_data(i) for i in data]
        elif isinstance(data, pygame.Surface):
            return ("SURFACE", pygame.image.tostring(data, "RGBA"), data.get_size())
        elif isinstance(data, pygame.Rect):
            return ("RECT", (data.x, data.y, data.w, data.h))
        return data

    def unpack_data(self, data):
        """Рекурсивно восстанавливает объекты Pygame из упакованных данных."""
        if isinstance(data, dict):
            return {k: self.unpack_data(v) for k, v in data.items()}
        elif isinstance(data, list):
            return [self.unpack_data(i) for i in data]
        elif isinstance(data, tuple) and len(data) > 0:
            if data[0] == "SURFACE":
                return pygame.image.fromstring(data[1], data[2], "RGBA")
            elif data[0] == "RECT":
                return pygame.Rect(data[1])
        return data

    def draw(self, screen):
        self.frame += 0.2
        # Отрисовка пустого шаблона карты
        pygame.draw.rect(screen, [40, 40, 40], self.gridBack)

        # Отрисовка кнопок
        for key in self.buttons:
            screen.blit(self.buttons[key]['img'][self.buttons[key]['state']], self.buttons[key]['rect'])


        # Здесь фон
        self.back_click()
        if 'background' in self.map:
            screen.blit(self.map['background']['image'], [32, 32])

        for item in self.gridRects:
            pygame.draw.rect(screen, 'Black', item, width=1)

        # Отрисовка палитры тайлов
        for i in range(len(self.tilesImages)):
            screen.blit(self.tilesImages[i], self.tilesPalleteRects[i])

        # Отрисовка палитры объектов
        for i in range(len(self.objectsImages)):
            screen.blit(self.objectsImages[i], self.objectsRects[i])

        # Отрисовка палитры анимированных объектов
        for i in range(len(self.animatedObjectsSprites)):
            current = self.frame % 4
            screen.blit(self.animatedObjectsSprites[i][int(current)], self.animatedObjectsRects[i])

        # Отрисовка фонов
        for i in range(len(self.back_names)):
            screen.blit(self.back_preview[i], self.back_preview_rects[i])

        # Отрисовка превью выбранного тайла
        self.pallete_click(screen)

        # Отрисовка карты
        self.grid_click()
        for key in self.map:
            if key != 'background' and not isinstance(self.map[key]['image'], list):
                screen.blit(self.map[key]['image'], self.map[key]['rect'])
            elif isinstance(self.map[key]['image'], list):
                current = self.frame % 4
                screen.blit(self.map[key]['image'][int(current)], self.map[key]['rect'])


        # Сохранение карты
        if pygame.mouse.get_pressed()[0]:
            if self.buttons['save']['rect'].collidepoint(pygame.mouse.get_pos()):
                self.save()
                self.buttons['save']['state'] = 1
            elif self.buttons['clear']['rect'].collidepoint(pygame.mouse.get_pos()):
                self.map = {}
                self.buttons['clear']['state'] = 1
