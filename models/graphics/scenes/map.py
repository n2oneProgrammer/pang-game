import pymunk
from pygame import Vector2

from models.enums.ColliderType import ColliderType
from models.enums.ObjectsCollisionType import ObjectCollisionType
from models.graphics.scenes.scene import Scene
from models.map_builder import MapBuilder
from models.objects.ball import Ball
from models.objects.ladder import Ladder
from models.objects.player import Player
from models.objects.sprite import Sprite


class Map(Scene):
    def __init__(self):
        super().__init__()
        self.space = pymunk.Space()
        self.space.gravity = 0, 100

        self.map_builder = MapBuilder("test_map.map")
        self.map_builder.load_background()
        self.objects = self.map_builder.get_elements(self.space)

        self.objects.append(Ladder("ladder.png", Vector2(300, 520), self.space, 40, 40))
        self.objects.append(Ladder("ladder.png", Vector2(380, 520), self.space, 40, 40))

    def update(self, delta_time):
        from models.game_manager import GameManager
        screen = GameManager().screen
        self.map_builder.draw_background(screen)

        self.space.step(delta_time)
        super().update(delta_time)
