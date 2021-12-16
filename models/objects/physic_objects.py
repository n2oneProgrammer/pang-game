import pymunk
from pygame.surface import Surface
from pygame.math import Vector2

from models.enums.ColliderType import ColliderType


class PhysicObject:

    def __init__(self, position: Vector2, space, velocity: Vector2 = Vector2(0, 0),
                 is_static: bool = True, width=0, height=0, collider_type=ColliderType.RECTANGLE):
        self.width = width
        self.height = height
        self.is_static = is_static
        self.space = space
        self.collider_type = collider_type
        self.body = pymunk.Body()
        self.position = position
        self.body.velocity = list(velocity)
        if self.is_static:
            self.body.body_type = pymunk.Body.STATIC
        else:
            self.body.body_type = pymunk.Body.DYNAMIC

    @property
    def position(self):
        return Vector2(self.body.position.x - self.width / 2, self.body.position.y - self.height / 2)

    @position.setter
    def position(self, value: Vector2):
        self.body.position = value.x + self.width / 2, value.y + self.height / 2

    @property
    def velocity(self):
        return Vector2(self.body.velocity)

    @velocity.setter
    def velocity(self, value: Vector2):
        self.body.velocity = value.x, value.y

    def draw(self, screen: Surface):
        pass
