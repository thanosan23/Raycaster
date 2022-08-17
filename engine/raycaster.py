import math
import pygame
from enum import Enum

from engine.level import *
from engine.utils.trig import DEGREE_TO_RADIANS, bound_radian
from engine.utils.colour import Colour

class Gridline(Enum):
    none = 0
    vertical = 1
    horizontal = 2

class Ray:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.angle = 0
        self.dist = 0

        self.gridline = Gridline.none

        self.depth_of_field = 0

        self.object = None

class Raycaster:
    def __init__(self, entity, block_size_x, block_size_y, fov=80):
        self.entity = entity
        self.block_size_x = block_size_x
        self.block_size_y = block_size_y
        self.fov = fov

        # NOTE: This can have a significant toll on framerate
        self.angle_per_iter = 8 # move 1/16 of an angle per iteration

        self.rays = []

        self.width = pygame.display.get_surface().get_width()
        self.height = pygame.display.get_surface().get_height()

        assert self.width % self.block_size_x == 0
        assert self.height % self.block_size_y == 0
        assert self.fov % 2 == 0

        self.mx = 0
        self.my = 0

        self.xo = 0
        self.yo = 0

    def cast_rays(self, level_manager):
        self.rays = []

        angle = bound_radian(self.entity.pos.angle - DEGREE_TO_RADIANS * self.fov / 2)
        level = level_manager.level
        # 1/16 of an angle per iteration
        for i in range(self.fov*self.angle_per_iter):
            ray = Ray()
            ray.angle = angle

            aTan = 1/(math.tan(ray.angle)) # secant of tangent
            distH = 1e20
            hx = self.entity.pos.x
            hy = self.entity.pos.y

            if ray.angle > math.pi:
                ray.y = ((int(self.entity.pos.y)//self.block_size_y)*self.block_size_y) - 1e-4
                ray.x = self.entity.pos.x - (self.entity.pos.y - ray.y) * aTan
                self.yo = -self.block_size_y
                self.xo = self.yo * aTan

            if ray.angle < math.pi:
                ray.y = ((int(self.entity.pos.y)//self.block_size_y)*self.block_size_y) + self.block_size_y
                ray.x =  self.entity.pos.x - (self.entity.pos.y - ray.y) * aTan
                self.yo = self.block_size_y
                self.xo = self.yo * aTan

            if ray.angle == 0 or ray.angle == math.pi:
                ray.x = self.entity.pos.x
                ray.y = self.entity.pos.y
                ray.depth_of_field = self.height // self.block_size_y

            while ray.depth_of_field < self.height // self.block_size_y:
                self.mx = int(ray.x) // self.block_size_y
                self.my = int(ray.y) // self.block_size_x
                self.mx = max(min(self.mx, len(level[0])-1), 0)
                self.my = max(min(self.my, len(level)-1), 0)

                ray.object = type(level[self.my][self.mx])

                if ray.object != Empty:
                    hx = ray.x
                    hy = ray.y
                    distH = math.dist((self.entity.pos.x, self.entity.pos.y), (hx, hy))
                    ray.depth_of_field = self.height // self.block_size_y
                else:
                    ray.x += self.xo
                    ray.y += self.yo
                    ray.depth_of_field += 1

            distV = 1e20
            vx = self.entity.pos.x
            vy = self.entity.pos.y

            ray.depth_of_field = 0
            nTan = math.tan(ray.angle)

            if ray.angle > math.pi/2 and ray.angle < 3*(math.pi/2):
                ray.x = (((int(self.entity.pos.x))//self.block_size_x)*self.block_size_x) - 1e-4
                ray.y = self.entity.pos.y - (self.entity.pos.x - ray.x) * nTan
                self.xo = -self.block_size_x
                self.yo = self.xo * nTan
            elif ray.angle < math.pi/2 or ray.angle > 3*(math.pi/2):
                ray.x = (((int(self.entity.pos.x)) // self.block_size_x) * self.block_size_x) + self.block_size_x
                ray.y =  self.entity.pos.y - (self.entity.pos.x - ray.x) * nTan
                self.xo = self.block_size_x
                self.yo = self.xo * nTan
            else:
                ray.x = self.entity.pos.x
                ray.y = self.entity.pos.y
                ray.depth_of_field = self.width // self.block_size_x

            while ray.depth_of_field < self.width // self.block_size_x:
                self.mx = int(ray.x) // self.block_size_x
                self.my = int(ray.y) // self.block_size_x
                self.mx = max(min(self.mx, len(level[0])-1), 0)
                self.my = max(min(self.my, len(level)-1), 0)

                ray.object = type(level[self.my][self.mx])

                if ray.object != Empty:
                    vx = ray.x
                    vy = ray.y
                    distV = math.dist((self.entity.pos.x, self.entity.pos.y), (vx, vy))
                    ray.depth_of_field = self.width // self.block_size_x
                else:
                    ray.x += self.xo
                    ray.y += self.yo
                    ray.depth_of_field += 1

            if distV < distH:
                ray.x = vx
                ray.y = vy
                ray.dist = distV
                ray.gridline = Gridline.vertical
            elif distH < distV:
                ray.x = hx
                ray.y = hy
                ray.dist = distH
                ray.gridline = Gridline.horizontal

            # fix fisheye effect
            ray.dist *= math.cos(bound_radian(self.entity.pos.angle - ray.angle))

            self.rays.append(ray)

            angle += (DEGREE_TO_RADIANS/self.angle_per_iter)
            angle = bound_radian(angle)

        return self.rays
