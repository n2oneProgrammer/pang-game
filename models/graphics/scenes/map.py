import pymunk
from pygame import Vector2

from models.enums.ColliderType import ColliderType
from models.enums.ObjectsCollisionType import ObjectCollisionType
from models.graphics.scenes.scene import Scene
from models.map_builder import MapBuilder
from models.objects.ball import Ball
from models.objects.player import Player
from models.objects.sprite import Sprite


class Map(Scene):
    def __init__(self):
        super().__init__()
        self.space = pymunk.Space()
        self.space.gravity = 0, 100

        self.map_builder = MapBuilder("test_map.map")
        self.objects = self.map_builder.get_elements(self.space)

        a = Ball("ball.png", Vector2(400, 300), self.space, 90 / 2, velocity=Vector2(150, 0))
        # b = Ball("ball.png", Vector2(600, 300), self.space, 10, velocity=Vector2(300, 10))

        self.objects.append(a)
        # self.objects.append(b)

        self.objects.append(Player(Vector2(40, 460), self.space, height=100))

    def update(self, delta_time):
        self.space.step(delta_time)
        super().update(delta_time)
