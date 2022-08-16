from engine.ecs import EntityManager
import pygame

class Game:
    def __init__(self, title, width, height):
        self.manager = EntityManager()
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption(title)
        self.clock = pygame.time.Clock()

        pygame.font.init()
        self.font_size=  15
        self.font = pygame.font.SysFont('Arial', 15)


    def run(self, update, draw, background_colour, fps=60, verbose=False):
        while True:
            self.screen.fill(background_colour.read_colour())
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit(0)

            update()
            draw(self.screen)

            if verbose:
                self.write(f"Raycaster", 0, 0)
                self.write(f"FPS: {self.clock.get_fps()}", 0, 0 + self.font_size)

            pygame.display.update()
            self.clock.tick(fps)

    def add_entity(self, entity):
        self.manager.add_entity(entity)


    def write(self, text, x, y, colour=(255, 255, 255)):
            surf = self.font.render(text, True, colour)
            self.screen.blit(surf, (x, y))

