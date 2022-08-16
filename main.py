import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

import math
import pygame

# self-made game framework (far from finished or polished)
from engine.game import Game
from engine.ecs import Entity
from engine.components import *
from engine.raycaster import Raycaster, Gridline
from engine.level import LevelManager, Wall
from engine.utils.colour import Colour

WIDTH = 1024
HEIGHT = 512

game = Game('Raycaster', WIDTH, HEIGHT)

level = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
         [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
         [1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
         [1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
         [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1],
         [1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1],
         [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
         [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]

level_manager = LevelManager(WIDTH, HEIGHT)
level_manager.set_level(level)

class Player(Entity):
    def __init__(self, x=0, y=0, w=5, h=5, angle=math.pi):
        self.pos = PositionComponent(x, y, w, h, angle=angle)
        self.keyboard = KeyboardComponent()
        self.collider = ColliderComponent(level_manager, WIDTH, HEIGHT)

    def update(self):
        self.keyboard.update()
        # bind keys to functions
        self.keyboard.bind(pygame.K_RIGHT, self.right)
        self.keyboard.bind(pygame.K_LEFT, self.left)
        self.keyboard.bind(pygame.K_UP, self.up)
        self.keyboard.bind(pygame.K_DOWN, self.down)

    def right(self):
        self.pos.turn(0.07)

    def left(self):
        self.pos.turn(-0.07)

    def up(self):
        updated_x = self.pos.x + self.pos.dx
        updated_y = self.pos.y + self.pos.dy
        if not self.collider.colliding(updated_x, updated_y, Wall):
            self.pos.x = updated_x
            self.pos.y = updated_y

    def down(self):
        updated_x = self.pos.x - self.pos.dx
        updated_y = self.pos.y - self.pos.dy
        if not self.collider.colliding(updated_x, updated_y, Wall):
            self.pos.x = updated_x
            self.pos.y = updated_y


player = Player(x=WIDTH//2, y=HEIGHT//2, w=8, h=8)
game.manager.add_entity(player)

player_raycaster = Raycaster(player, int(WIDTH/len(level[0])), int(HEIGHT/len(level)), fov=70)

def update():
    game.manager.update()
    player_raycaster.cast_rays(level_manager)

def draw(screen):
    for i, ray in enumerate(player_raycaster.rays):
        # shading
        if ray.object == Wall:
            colour = Colour(255, 0, 0)
            if ray.gridline == Gridline.horizontal:
                colour.darken()

            dist = (player_raycaster.block_size_y * HEIGHT) / ray.dist
            dist = min(HEIGHT, dist)
            offset = (HEIGHT - dist) / 2

            render_width = int(WIDTH / player_raycaster.fov) + 1
            pygame.draw.line(screen, colour.read_colour(), (i*render_width, offset), (i*render_width, dist + offset), render_width)

if __name__ == "__main__":
    game.run(update, draw, fps=60, verbose=True)
