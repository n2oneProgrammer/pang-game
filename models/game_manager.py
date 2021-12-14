import pygame

from models.graphics.scenes.map import Map
from utilities.singleton import Singleton


class GameManager(metaclass=Singleton):
    def __init__(self, width=800, height=600):
        self.width = width
        self.height = height

        self._clock = pygame.time.Clock()
        self.screen = None

    def run(self):
        pygame.init()

        self.screen = pygame.display.set_mode([self.width, self.height])

        scene = Map()

        running = True
        while running:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            self.screen.fill((255, 255, 255))
            if self._clock.get_fps() == 0:
                dt = 0
            else:
                dt = 1.0 / self._clock.get_fps()
            scene.update(dt)
            pygame.display.flip()
            self._clock.tick(60)

            pygame.display.set_caption("fps: " + str(self._clock.get_fps()))
        pygame.quit()
