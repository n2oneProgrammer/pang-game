import os
import pygame
from pygame.surface import Surface
from pygame.math import Vector2

from models.objects.physic_objects import PhysicObject


class Sprite(PhysicObject):
    def __init__(self, path, position: Vector2, width = None, height = None,
                 velocity: Vector2 = Vector2(0, 0),
                 acceleration: Vector2 = Vector2(0, 0),
                 is_static: bool = False):
        super().__init__(position, velocity, acceleration, is_static)
        self.path = os.path.join('assets', path)
        self.width = width
        self.height = height

    def draw(self, screen: Surface):
        loaded_img = pygame.image.load(self.path)
        scaled_img = pygame.transform.scale(loaded_img, (self.width, self.height)) 
        screen.blit(scaled_img, (self.position[0], self.position[1]))
