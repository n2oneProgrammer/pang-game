import time
from pygame import Vector2, Surface

import models.game_manager
from models.enums.ColliderType import ColliderType
from models.enums.ObjectsCollisionType import ObjectCollisionType
from models.objects.sprite import Sprite


class ChainBullet:
    def __init__(self, position: Vector2, space):

        self.chain_src_1 = "chain1.png"
        self.chain_src_2 = "chain2.png"
        self.chain_head_src = "chainhead.png"
        self.start_img_1 = True
        self.width = 50

        first_chain_element = Sprite(self.chain_src_1, position, space, width=self.width, is_static=True,
                                     collision_type=ColliderType.RECTANGLE)

        list(first_chain_element.body.shapes)[0].collision_type = ObjectCollisionType.CHAIN
        self.chains_elements = [first_chain_element]
        self.space = space
        self.height = first_chain_element.height
        self.last_position = position
        self.last_increasing = time.time()
        self.head = Sprite(self.chain_head_src, position, space, width=self.width, is_static=True,
                           collision_type=ColliderType.RECTANGLE)

        hit_collision_handler = space.add_collision_handler(ObjectCollisionType.CHAIN, ObjectCollisionType.BALL)
        hit_collision_handler.begin = self.hit_ball

    def hit_ball(self, data, space, other):
        for s in data.shapes:
            if s.collision_type == ObjectCollisionType.CHAIN:
                for obj in self.chains_elements:
                    shape = list(obj.body.shapes)[0]
                    if shape is s:
                        self.delete_self()
                        break

            if s.collision_type == ObjectCollisionType.BALL:
                for obj in models.game_manager.GameManager().scene.objects:
                    shape = list(obj.body.shapes)[0]
                    if shape is s:
                        obj.split()
                        break
        return True

    def draw(self, screen: Surface):
        if self.last_position[1] < 0:
            self.delete_self()
        if time.time() - self.last_increasing > 0.2:
            self.last_increasing = time.time()
            self.increase_chain()

            for index, element in enumerate(self.chains_elements):
                if self.start_img_1 != (index % 2 == 0):
                    element.change_img_src(self.chain_src_1)
                else:
                    element.change_img_src(self.chain_src_2)
            self.start_img_1 = not self.start_img_1
        for element in self.chains_elements:
            element.draw(screen)

        self.head.position = self.last_position - Vector2(0, self.head.height)
        self.head.draw(screen)

    def increase_chain(self):
        self.last_position -= Vector2(0, self.height)

        chain_element = Sprite(self.chain_src_1, self.last_position, self.space, width=self.width, is_static=True,
                               collision_type=ColliderType.RECTANGLE)
        list(chain_element.body.shapes)[0].collision_type = ObjectCollisionType.CHAIN
        self.chains_elements.append(chain_element)

    def delete_self(self):
        for element in self.chains_elements:
            self.space.remove(list(element.body.shapes)[0], element.body)

        from models.game_manager import GameManager
        if self in GameManager().scene.bullets:
            GameManager().scene.bullets.remove(self)
