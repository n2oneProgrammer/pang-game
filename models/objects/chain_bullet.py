import time
from pygame import Vector2, Surface
from models.enums.ColliderType import ColliderType
from models.enums.ObjectsCollisionType import ObjectCollisionType
from models.objects.sprite import Sprite


class ChainBullet:
    def __init__(self, position: Vector2, space):
        first_chain_element = Sprite("chain1.png", position, space, width=50, is_static=True,
                                     collision_type=ColliderType.RECTANGLE)
        list(first_chain_element.body.shapes)[0].collision_type = ObjectCollisionType.CHAIN
        self.chains_elements = [first_chain_element]
        self.space = space
        self.height = first_chain_element.height
        self.last_position = position
        self.last_increasing = time.time()

    def draw(self, screen: Surface):
        if self.last_position[1] < 0:
            self.delete_self()
        if time.time() - self.last_increasing > 0.2:
            self.last_increasing = time.time()
            self.increase_chain()

        for element in self.chains_elements:
            element.draw(screen)

    def increase_chain(self):
        self.last_position -= Vector2(0, self.height)
        self.chains_elements.append(
            Sprite("chain1.png", self.last_position, self.space, width=50, is_static=True,
                   collision_type=ColliderType.RECTANGLE))

    def delete_self(self):
        for element in self.chains_elements:
            self.space.remove(list(element.body.shapes)[0], element.body)

        from models.game_manager import GameManager
        GameManager().scene.bullets.remove(self)
