from pygame.surface import Surface


class PhysicObject:

    def __init__(self, position: list[int], velocity=None, acceleration=None,
                 is_static: bool = False):
        if acceleration is None:
            acceleration = [0, 0]
        if velocity is None:
            velocity = [0, 0]
        self.position = position
        self.velocity = velocity
        self.acceleration = acceleration
        self.is_static = is_static

    def draw(self, screen: Surface):
        pass

    def calc_position(self, delta_time):
        if self.is_static:
            return
        self.position[0] += delta_time * self.velocity[0]
        self.position[1] += delta_time * self.velocity[1]

    def calc_velocity(self, delta_time):
        if self.is_static:
            return
        self.velocity[0] += delta_time * self.acceleration[0]
        self.velocity[1] += delta_time * self.acceleration[1]
