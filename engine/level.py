import pygame

class MapObject:
    def __init__(self, x=0, y=0, w=0, h=0):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

class Empty(MapObject):
    def __init__(self, x=0, y=0, w=0, h=0):
        super().__init__(x, y, w, h)

class Wall(MapObject):
    def __init__(self, x=0, y=0, w=0, h=0):
        super().__init__(x, y, w, h)

class LevelManager:
    def __init__(self, screen_width, screen_height):
        self.level = None
        self.screen_width = screen_width
        self.screen_height = screen_height

    def set_level(self, level):
        self.level = [[0 for i in range(len(level[0]))] for j in range(len(level)) ]
        assert self.screen_width % len(self.level[0]) == 0
        assert self.screen_height % len(self.level) == 0
        block_size_y = self.screen_width / len(self.level)
        block_size_x = self.screen_height / len(self.level[0])
        for y in range(len(level)):
            for x in range(len(level[0])):
                if level[y][x] == 1:
                    self.level[y][x] = Wall(x * block_size_x, y * block_size_y, block_size_x, block_size_y)
                else:
                    self.level[y][x] = Empty(x * block_size_x, y * block_size_y, block_size_x, block_size_y)
