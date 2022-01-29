import math
import time

import pymunk
from pygame import Vector2, Surface

from models.enums.ColliderType import ColliderType
from models.enums.ObjectsCollisionType import ObjectCollisionType
from models.objects.sprite import Sprite


class Ladder(Sprite):

    def __init__(self, path, position: Vector2, space, width=None, height=None):
        super().__init__(path, position, space, width, height, Vector2(0, 0), True, ColliderType.RECTANGLE)
        shape = list(self.body.shapes)[0]
        shape.collision_type = ObjectCollisionType.LADDER
        shape.filter = pymunk.ShapeFilter(categories=ObjectCollisionType.LADDER,
                                          mask=pymunk.ShapeFilter.ALL_MASKS())
