import os
import unittest
from unittest.mock import Mock

from models.map_builder import MapBuilder
from models.objects.sprite import Sprite


class MapBuilderConstructSpriteTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.map_builder = MapBuilder("src")

    # TYPE SPRITE
    def test_type_sprite_require_no_asset(self):
        map_object = {
            "type": "sprite",
            "position": [0, 0],
            "size": [0, 0]
        }

        with self.assertRaises(ValueError):
            self.map_builder.construct_object(map_object, None)

    def test_type_sprite_require_no_position(self):
        map_object = {
            "type": "sprite",
            "asset": "asset name",
            "size": [0, 0]
        }

        with self.assertRaises(ValueError):
            self.map_builder.construct_object(map_object, None)

    def test_type_sprite_require_no_size(self):
        map_object = {
            "type": "sprite",
            "asset": "asset name",
            "position": [0, 0]
        }

        with self.assertRaises(ValueError):
            self.map_builder.construct_object(map_object, None)

    def test_type_sprite_not_found_asset(self):
        map_object = {
            "type": "sprite",
            "asset": "asset name",
            "position": [0, 0],
            "size": [0, 0]
        }
        self.map_builder.assets = []

        self.assertRaises(ValueError, self.map_builder.construct_object, map_object, None)

    def test_type_sprite_returning_object(self):
        map_object = {
            "type": "sprite",
            "asset": "asset name",
            "position": [0, 0],
            "size": [0, 0]
        }
        self.map_builder.assets = [
            {"name": "asset name", "src": "random_sprite.png"}
        ]
        Sprite.prepare_img = Mock(return_value=None)

        result = self.map_builder.construct_object(map_object, None)
        self.assertEqual(len(result), 1)
        result = result[0]
        self.assertIsInstance(result, Sprite)
        self.assertEqual(os.path.normpath(result.path), os.path.normpath("assets/random_sprite.png"))
