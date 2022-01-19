import os.path
import unittest
from unittest.mock import Mock

import pymunk
from pygame import Vector2

from models.enums.ColliderType import ColliderType
from models.objects.sprite import Sprite


class SpriteTest(unittest.TestCase):
    def assumptions_required_options_test(self):
        Sprite.prepare_img = Mock()

        sprite = Sprite("test_img.png", Vector2(10, 20), None, width=200, height=300)

        self.assertEqual(os.path.normpath("assets/test_img.png"), os.path.normpath(sprite.path))
        self.assertIsInstance(sprite.poly, pymunk.Poly)
        self.assertEqual(1, sprite.poly.elasticity)

    def assumptions_collision_type_circle_test(self):
        Sprite.prepare_img = Mock()

        sprite = Sprite("test_img.png", Vector2(10, 20), None, width=200, height=300,
                        collision_type=ColliderType.CIRCLE)

        self.assertIsInstance(sprite.poly, pymunk.Circle)

    def change_img_src_test(self):
        Sprite.prepare_img = Mock()

        sprite = Sprite("test_img2.png", Vector2(10, 20), None, width=200, height=300)

        self.assertEqual(os.path.normpath("assets/test_img2.png"), os.path.normpath(sprite.path))

