import pymunk
from pygame import Vector2

from models.enums.ColliderType import ColliderType
from models.graphics.scenes.scene import Scene
from models.map_builder import MapBuilder
from models.objects.sprite import Sprite


class Map(Scene):
    def __init__(self):
        super().__init__()
        self.space = pymunk.Space()
        self.space.gravity = 0, 100

        self.map_builder = MapBuilder("test_map.map")
        self.objects = self.map_builder.get_elements(self.space)

        # Create this ball is temporary(for testing)
        # TODO: remove later
        a = Sprite("ball.png", Vector2(400, 300), self.space, width=45, collision_type=ColliderType.CIRCLE)
        a.body.body_type = pymunk.Body.DYNAMIC
        a.body.velocity = 400, -300

        b = Sprite("ball.png", Vector2(600, 300), self.space, width=45, collision_type=ColliderType.CIRCLE)
        b.body.body_type = pymunk.Body.DYNAMIC
        b.body.velocity = 300, 0
        self.objects.append(a)
        self.objects.append(b)

    def update(self, delta_time):
        self.space.step(delta_time)
        for obj in self.objects:
            from models.game_manager import GameManager
            obj.draw(GameManager().screen)
