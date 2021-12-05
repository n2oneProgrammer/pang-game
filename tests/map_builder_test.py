import os
import unittest
from unittest.mock import Mock

from pygame.math import Vector2

from models.map_builder import MapBuilder
from models.objects.rectangle import Rectangle


class MapBuilderConstructAssetTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.map_builder = MapBuilder("src")

    def test_check_requires_no_name(self):
        asset_json = {
            "src": "image.png"
        }

        with self.assertRaises(ValueError):
            self.map_builder.construct_asset(asset_json)

    def test_check_requires_no_src(self):
        asset_json = {
            "name": "name asset"
        }

        with self.assertRaises(ValueError):
            self.map_builder.construct_asset(asset_json)

    def test_checking_file_exit(self):
        asset_json = {
            "name": "name asset",
            "src": "test_case_not_exit.png"
        }

        with self.assertRaises(FileNotFoundError):
            self.map_builder.construct_asset(asset_json)

    def test_returning_object(self):
        asset_json = {
            "name": "name asset",
            "src": "test_case_exit.png"
        }
        os.path.exists = Mock(return_value=True)

        result = self.map_builder.construct_asset(asset_json)

        self.assertEqual(result["name"], "name asset")
        self.assertEqual(result["src"], "assets\\test_case_exit.png")


class MapBuilderConstructObjectTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.map_builder = MapBuilder("src")

    def test_check_require_no_type(self):
        map_object = {
            "position": [0, 0],
            "size": [0, 0]
        }

        with self.assertRaises(ValueError):
            self.map_builder.construct_object(map_object)

    def test_type_no_implement(self):
        map_object = {
            "type": "undefined type",
            "position": [0, 0],
            "size": [0, 0]
        }

        with self.assertRaises(NotImplementedError):
            self.map_builder.construct_object(map_object)

    # TYPE SPRITE
    def test_type_sprite_check_require_no_asset(self):
        map_object = {
            "type": "sprite",
            "position": [0, 0],
            "size": [0, 0]
        }

        with self.assertRaises(ValueError):
            self.map_builder.construct_object(map_object)

    def test_type_sprite_check_require_no_position(self):
        map_object = {
            "type": "sprite",
            "asset": "asset name",
            "size": [0, 0]
        }

        with self.assertRaises(ValueError):
            self.map_builder.construct_object(map_object)

    def test_type_sprite_check_require_no_size(self):
        map_object = {
            "type": "sprite",
            "asset": "asset name",
            "position": [0, 0]
        }

        with self.assertRaises(ValueError):
            self.map_builder.construct_object(map_object)

    def test_type_sprite_returning_object(self):
        map_object = {
            "type": "sprite",
            "asset": "asset name",
            "position": [0, 0],
            "size": [0, 0]
        }
        # TODO(n2one): Change to sprite object
        expect = [None]

        result = self.map_builder.construct_object(map_object)

        self.assertEqual(result, expect)

    # TYPE RECT
    def test_type_rect_check_require_no_color(self):
        map_object = {
            "type": "rect",
            "position": [0, 0],
            "size": [0, 0]
        }

        with self.assertRaises(ValueError):
            self.map_builder.construct_object(map_object)

    def test_type_rect_check_require_no_position(self):
        map_object = {
            "type": "rect",
            "color": "#000000",
            "size": [0, 0]
        }

        with self.assertRaises(ValueError):
            self.map_builder.construct_object(map_object)

    def test_type_rect_check_require_no_size(self):
        map_object = {
            "type": "rect",
            "color": "#000000",
            "position": [0, 0]
        }

        with self.assertRaises(ValueError):
            self.map_builder.construct_object(map_object)

    def test_type_rect_returning_object(self):
        map_object = {
            "type": "rect",
            "color": "#123456",
            "position": [40, 10],
            "size": [30, 20]
        }
        expect = Rectangle(
            width=30,
            height=20,
            position=Vector2(40, 10),
            color="#123456"
        )

        result = self.map_builder.construct_object(map_object)[0]
        self.assertIsInstance(result, Rectangle)
        self.assertEqual(result.position, expect.position)
        self.assertEqual(result.width, expect.width)
        self.assertEqual(result.height, expect.height)
        self.assertEqual(result.color, expect.color)