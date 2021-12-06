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
        self.img = self.prepare_img()


    def prepare_img(self):
        loaded_img = pygame.image.load(self.path)
        w, h = (loaded_img.get_width(), loaded_img.get_height())

        if self.width:
            if self.height:
                w, h = self.width, self.height
            else:
                h = h * self.width / w
                w = self.width
        elif self.height:
            w = w * self.height / h
    
        scaled_img = pygame.transform.scale(loaded_img, (w, h))

        return scaled_img


    def draw(self, screen: Surface):
        screen.blit(self.img, self.position)
