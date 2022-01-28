import os
import unittest
from unittest.mock import Mock

from models.map_builder import MapBuilder
from models.objects.ball import Ball
from models.objects.sprite import Sprite


class MapBuilderConstructBallTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.map_builder = MapBuilder("src")

    # TYPE BALL
    def test_type_ball_require_no_asset(self):
        map_object = {
            "type": "ball",
            "position": [0, 0],
            "radius": 10,
            "start_velocity": [0, 0]
        }

        with self.assertRaises(ValueError):
            self.map_builder.construct_object(map_object, None)

    def test_type_ball_require_no_position(self):
        map_object = {
            "type": "ball",
            "asset": "asset name",
            "radius": 10,
            "start_velocity": [0, 0]
        }

        with self.assertRaises(ValueError):
            self.map_builder.construct_object(map_object, None)

    def test_type_ball_require_no_radius(self):
        map_object = {
            "type": "ball",
            "asset": "asset name",
            "position": [0, 0],
            "start_velocity": [0, 0]
        }

        with self.assertRaises(ValueError):
            self.map_builder.construct_object(map_object, None)

    def test_type_ball_require_no_start_velocity(self):
        map_object = {
            "type": "ball",
            "asset": "asset name",
            "position": [0, 0],
            "radius": 10
        }

        with self.assertRaises(ValueError):
            self.map_builder.construct_object(map_object, None)

    def test_type_ball_not_found_asset(self):
        map_object = {
            "type": "ball",
            "asset": "asset name",
            "position": [0, 0],
            "radius": 10,
            "start_velocity": [0, 0]
        }
        self.map_builder.assets = []

        self.assertRaises(ValueError, self.map_builder.construct_object, map_object, None)

    def test_type_ball_returning_object(self):
        map_object = {
            "type": "ball",
            "asset": "asset name",
            "position": [0, 0],
            "radius": 10,
            "start_velocity": [20, -10]
        }
        self.map_builder.assets = [
            {"name": "asset name", "src": "random_sprite.png"}
        ]
        Sprite.prepare_img = Mock(return_value=None)

        result = self.map_builder.construct_object(map_object, None)
        self.assertEqual(len(result), 1)
        result = result[0]
        self.assertIsInstance(result, Ball)
        self.assertEqual(result.width, 20)
        self.assertEqual(result.velocity.x, 20)
        self.assertEqual(result.velocity.y, -10)
        self.assertEqual(os.path.normpath(result.path), os.path.normpath("assets/random_sprite.png"))
