import pygame
from pygame.math import Vector2
from pygame.surface import Surface

from models.objects.physic_objects import PhysicObject
from utilities.converters import Converters


class Rectangle(PhysicObject):
    def __init__(self, position: Vector2, width: int, height: int, color: str = "#000000",
                 velocity: Vector2 = Vector2(0, 0),
                 acceleration: Vector2 = Vector2(0, 0),
                 is_static: bool = False):
        super().__init__(position, velocity, acceleration, is_static)
        self.width = width
        self.height = height

        self.color = Converters.color_str_to_tuple(color)

    def draw(self, screen: Surface):
        pygame.draw.rect(screen, (30, 90, 200),
                         pygame.Rect(self.position[0], self.position[1], self.width, self.height))
