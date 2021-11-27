from models.graphics.scenes.map import Map
import pygame

from models.graphics.scenes.map import Map
from utilities.singleton import Singleton


class GameManager(metaclass=Singleton):
    def __init__(self, width=800, height=600):
        self.width = width
        self.height = height
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
            scene.update()
            pygame.display.flip()
        pygame.quit()
