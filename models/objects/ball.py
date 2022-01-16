import pymunk
from pygame import Vector2

from models.enums.ColliderType import ColliderType
from models.enums.ObjectsCollisionType import ObjectCollisionType
from models.objects.sprite import Sprite


class Ball(Sprite):
    def __init__(self, path, position: Vector2, space, radius,
                 velocity: Vector2 = Vector2(0, 0),
                 is_static: bool = False):
        super().__init__(path, position, space, 2 * radius, 2 * radius, velocity, is_static, ColliderType.CIRCLE)
        list(self.body.shapes)[0].collision_type = ObjectCollisionType.BALL
