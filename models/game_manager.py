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
        self.scene = None

    def end_game(self):
        self.running = False

    def run(self):
        pygame.init()

        self.screen = pygame.Surface([800, 600])
        self.screen2 = pygame.display.set_mode([self.width, self.height], pygame.RESIZABLE)

        self.scene = Map()

        while self.running:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.VIDEORESIZE:
                    self.width = event.w
                    self.height = event.h
                elif self.player is not None:
                    self.player.run_events(event)
            if self._clock.get_fps() == 0:
                dt = 0
            else:
                dt = 1.0 / self._clock.get_fps()
            self.scene.update(dt)
            resize_screen = pygame.transform.scale(self.screen, (self.width, self.height))
            self.screen2.blit(resize_screen, (0, 0))
            pygame.display.flip()
            self._clock.tick(60)

            pygame.display.set_caption("fps: " + str(self._clock.get_fps()))
        pygame.quit()
