import pygame
from pygame.surface import Surface

from models.objects.physic_objects import PhysicObject


class Rectangle(PhysicObject):
    def __init__(self, position: tuple, width: int, height: int, velocity: tuple = (0, 0), acceleration: tuple = (0, 0),
                 is_static: bool = False):
        super().__init__(position, velocity, acceleration, is_static)
        self.width = width
        self.height = height

    def draw(self, screen: Surface):
        pygame.draw.rect(screen, (30, 90, 200),
                         pygame.Rect(self.position[0], self.position[1], self.width, self.height))
