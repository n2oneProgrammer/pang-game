import pygame
import pymunk
from pygame.math import Vector2
from pygame.surface import Surface

from models.objects.physic_objects import PhysicObject
from utilities.converters import Converters


class Rectangle(PhysicObject):
    def __init__(self, position: Vector2, width: int, height: int, space, color: str = "#000000",
                 velocity: Vector2 = Vector2(0, 0),
                 is_static: bool = False):
        super().__init__(position, space, velocity, is_static, width, height)

        self.poly = pymunk.Poly.create_box(self.body, size=(width, height))
        self.poly.mass = 10
        self.poly.elasticity = 1
        self.poly.friction = 0
        if self.space is not None:
            self.space.add(self.body, self.poly)

        self.color = Converters.color_str_to_tuple(color)

    def draw(self, screen: Surface):
        pygame.draw.rect(screen, (30, 90, 200),
                         pygame.Rect(self.position.x, self.position.y,
                                     self.width, self.height))
