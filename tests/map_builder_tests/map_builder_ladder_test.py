import os
import unittest
from unittest.mock import Mock

from models.enums.ObjectsCollisionType import ObjectCollisionType
from models.map_builder import MapBuilder
from models.objects.ball import Ball
from models.objects.ladder import Ladder
from models.objects.sprite import Sprite


class MapBuilderConstructLadderTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.map_builder = MapBuilder("src")

    # TYPE LADDER
    def test_type_ladder_require_no_asset(self):
        map_object = {
            "type": "ladder",
            "position": [0, 0],
            "size": [40, 40]
        }

        with self.assertRaises(ValueError):
            self.map_builder.construct_object(map_object, None)

    def test_type_ladder_require_no_position(self):
        map_object = {
            "type": "ladder",
            "asset": "asset name",
            "size": [40, 40]
        }

        with self.assertRaises(ValueError):
            self.map_builder.construct_object(map_object, None)

    def test_type_ladder_require_no_size(self):
        map_object = {
            "type": "ladder",
            "asset": "asset name",
            "position": [0, 0]
        }

        with self.assertRaises(ValueError):
            self.map_builder.construct_object(map_object, None)

    def test_type_ladder_not_found_asset(self):
        map_object = {
            "type": "ladder",
            "asset": "asset name",
            "position": [0, 0],
            "size": [40, 40]
        }
        self.map_builder.assets = []

        self.assertRaises(ValueError, self.map_builder.construct_object, map_object, None)

    def test_type_ladder_returning_object(self):
        map_object = {
            "type": "ladder",
            "asset": "asset name",
            "position": [0, 0],
            "size": [40, 40]
        }
        self.map_builder.assets = [
            {"name": "asset name", "src": "random_sprite.png"}
        ]
        Sprite.prepare_img = Mock(return_value=None)

        result = self.map_builder.construct_object(map_object, None)
        self.assertEqual(len(result), 1)
        result = result[0]
        self.assertIsInstance(result, Ladder)
        self.assertEqual(result.width, 40)
        self.assertEqual(os.path.normpath(result.path), os.path.normpath("assets/random_sprite.png"))
        self.assertEqual(ObjectCollisionType.LADDER, list(result.body.shapes)[0].collision_type)
