import os
import pygame
import pymunk
from pygame.surface import Surface
from pygame.math import Vector2

from models.enums.ColliderType import ColliderType
from models.objects.physic_objects import PhysicObject


class Sprite(PhysicObject):
    def __init__(self, path, position: Vector2, space, width=None, height=None,
                 velocity: Vector2 = Vector2(0, 0),
                 is_static: bool = False, collision_type=ColliderType.RECTANGLE):
        self.width = width
        self.height = height
        self.path = os.path.join('assets', path)
        self.img = self.prepare_img()

        super().__init__(position, space, velocity, is_static, self.width, self.height, collision_type)

        if self.collider_type == ColliderType.RECTANGLE:
            self.poly = pymunk.Poly.create_box(self.body, size=(self.width, self.height))
        elif self.collider_type == ColliderType.CIRCLE:
            self.poly = pymunk.Circle(self.body, self.width / 2)
        else:
            raise ValueError("I dont recognise collider type")

        self.poly.mass = 10
        self.poly.elasticity = 1

        if self.space is not None:
            self.space.add(self.body, self.poly)

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

        self.width = w
        self.height = h

        scaled_img = pygame.transform.scale(loaded_img, (w, h))

        return scaled_img

    def draw(self, screen: Surface):
        screen.blit(self.img, self.position)
