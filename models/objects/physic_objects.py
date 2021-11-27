from pygame.surface import Surface
from pygame.math import Vector2


class PhysicObject:

    def __init__(self, position: Vector2, velocity: Vector2 = Vector2(0, 0), acceleration: Vector2 = Vector2(0, 0),
                 is_static: bool = False):
        self.position = position
        self.velocity = velocity
        self.acceleration = acceleration
        self.is_static = is_static

    def draw(self, screen: Surface):
        pass

    def calc_position(self, delta_time):
        if self.is_static:
            return
        self.position += delta_time * self.velocity

    def calc_velocity(self, delta_time):
        if self.is_static:
            return
        self.velocity += delta_time * self.acceleration
