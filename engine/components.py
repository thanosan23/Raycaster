import pygame
import math

from engine.ecs import Component
from engine.utils.trig import bound_radian
from engine.level import MapObject, Empty

class PositionComponent(Component):
    def __init__(self, x, y, w, h, dx=0, dy=0, angle=0, angle_step_size=3):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

        self.dx = dx
        self.dy = dy

        # angle is in radians
        self.angle = angle
        self.angle_step_size = angle_step_size

    def turn(self, turn_size):
        self.angle = bound_radian(self.angle + turn_size)
        self.dx = math.cos(self.angle) * self.angle_step_size
        self.dy = math.sin(self.angle) * self.angle_step_size

class SpriteRendererComponent(Component):
    def __init__(self, w, h, colour):
        self.surface = pygame.Surface((w, h))
        self.surface.fill(colour)
    def draw(self, screen, pos : PositionComponent, draw_angle=False):
        screen.blit(self.surface, (pos.x, pos.y))
        if draw_angle:
            pygame.draw.line(screen, (0, 255, 0), (pos.x, pos.y), (pos.x + pos.dx * pos.angle_step_size, pos.y + pos.dy * pos.angle_step_size))

class KeyboardComponent(Component):
    def __init__(self):
        self.keys = None
    def update(self):
        self.keys = pygame.key.get_pressed()
    def bind(self, key, action):
        if self.keys[key]:
            action()

class ColliderComponent(Component):
    def __init__(self, level, screen_width, screen_height):
        self.level = level
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.block_size_x = self.screen_width / len(self.level.level[0])
        self.block_size_y = self.screen_height / len(self.level.level)

    def colliding(self, x, y, mapObject):
        assert isinstance(mapObject(), MapObject)
        assert not isinstance(mapObject(), Empty)
        if x > self.screen_width or y > self.screen_height or x < 0 or y < 0:
            return True
        x = int(x // self.block_size_x)
        y = int(y // self.block_size_y)
        return isinstance(self.level.level[y][x], mapObject)
