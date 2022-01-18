import math

import pymunk
from pygame import Vector2

from models.enums.ColliderType import ColliderType
from models.enums.ObjectsCollisionType import ObjectCollisionType
from models.objects.sprite import Sprite


class Ball(Sprite):
    PERCENT_LOSS_ENERGY = 3 / 10
    ANGLE_SPLIT_BALL = 20 * math.pi / 180
    MIN_RADIUS = 10

    def __init__(self, path, position: Vector2, space, radius,
                 velocity: Vector2 = Vector2(0, 0),
                 is_static: bool = False):
        super().__init__(path, position, space, 2 * radius, 2 * radius, velocity, is_static, ColliderType.CIRCLE)
        list(self.body.shapes)[0].collision_type = ObjectCollisionType.BALL

    def split(self):
        self.space.remove(list(self.body.shapes)[0], self.body)
        from models.game_manager import GameManager
        GameManager().scene.objects.remove(self)

        if self.width / 4 < self.MIN_RADIUS:
            return

        # calc velocity from energy
        velocity = self.velocity.length()
        stage1 = 2 * (1 - self.PERCENT_LOSS_ENERGY) * velocity * velocity
        stage2 = 2 * self.PERCENT_LOSS_ENERGY * self.space.gravity[1] * (600 - self.position.y)

        new_velocity = math.sqrt(stage1 + stage2)

        x_velocity = new_velocity * math.sin(self.ANGLE_SPLIT_BALL)
        y_velocity = new_velocity * math.cos(self.ANGLE_SPLIT_BALL)

        ball1 = Ball(self.path[7:], self.position - Vector2(self.width / 4, 0), self.space, self.width / 4,
                     velocity=Vector2(-x_velocity, -y_velocity))
        ball2 = Ball(self.path[7:], self.position + Vector2(self.width / 4, 0), self.space, self.width / 4,
                     velocity=Vector2(x_velocity, -y_velocity))

        GameManager().scene.objects.append(ball1)
        GameManager().scene.objects.append(ball2)
