import pygame

from models.graphics.scenes.map import Map
from utilities.singleton import Singleton


class GameManager(metaclass=Singleton):
    def __init__(self, width=800, height=600):
        self.width = width
        self.height = height

        self._clock = pygame.time.Clock()
        self.screen = None
        self.running = True
        self.player = None

    def end_game(self):
        self.running = False

    def run(self):
        pygame.init()

        self.screen = pygame.display.set_mode([self.width, self.height])

        scene = Map()

        while self.running:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif self.player is not None:
                    self.player.run_events(event)
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
