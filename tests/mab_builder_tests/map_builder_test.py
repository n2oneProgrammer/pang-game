import json
import os
import unittest
from unittest.mock import Mock, patch, mock_open, MagicMock

from pygame.math import Vector2

from models.map_builder import MapBuilder


class MapBuilderConstructAssetTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.map_builder = MapBuilder("src")

    def test_requires_no_name(self):
        asset_json = {
            "src": "image.png"
        }

        with self.assertRaises(ValueError):
            self.map_builder.construct_asset(asset_json)

    def test_requires_no_src(self):
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
        self.assertEqual(result["src"], "test_case_exit.png")


class MapBuilderConstructObjectTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.map_builder = MapBuilder("src")

    def test_require_no_type(self):
        map_object = {
            "position": [0, 0],
            "size": [0, 0]
        }

        with self.assertRaises(ValueError):
            self.map_builder.construct_object(map_object, None)

    def test_type_no_implement(self):
        map_object = {
            "type": "undefined type",
            "position": [0, 0],
            "size": [0, 0]
        }

        with self.assertRaises(NotImplementedError):
            self.map_builder.construct_object(map_object, None)


    # STRETCH OPTIONS
    def test_stretch_require_no_start_position(self):
        map_object = {
            "type": "rect",
            "color": "#000000",
            "size": [10, 10],
            "stretch": "yes",
            "end-position": [30, 10]
        }

        with self.assertRaises(ValueError):
            self.map_builder.construct_object(map_object, None)

    def test_stretch_require_no_end_position(self):
        map_object = {
            "type": "rect",
            "color": "#000000",
            "size": [10, 10],
            "stretch": "yes",
            "start-position": [0, 0]
        }

        with self.assertRaises(ValueError):
            self.map_builder.construct_object(map_object, None)

    def test_stretch_x(self):
        map_object = {
            "type": "rect",
            "color": "#000000",
            "size": [10, 10],
            "stretch": "yes",
            "start-position": [0, 30],
            "end-position": [100, 30]
        }

        result = self.map_builder.construct_object(map_object, MagicMock())

        self.assertEqual(len(result), 10)
        for i in range(0, 10):
            self.assertEqual(result[i].position, Vector2(i * 10, 30))

    def test_stretch_y(self):
        map_object = {
            "type": "rect",
            "color": "#000000",
            "size": [10, 10],
            "stretch": "yes",
            "start-position": [30, 0],
            "end-position": [30, 100]
        }

        result = self.map_builder.construct_object(map_object, MagicMock())

        self.assertEqual(len(result), 10)
        for i in range(0, 10):
            self.assertEqual(result[i].position, Vector2(30, i * 10))

    def test_stretch_xy(self):
        map_object = {
            "type": "rect",
            "color": "#000000",
            "size": [10, 10],
            "stretch": "yes",
            "start-position": [0, 0],
            "end-position": [100, 100]
        }

        result = self.map_builder.construct_object(map_object, MagicMock())

        self.assertEqual(len(result), 100)
        for i in range(0, 10):
            for j in range(0, 10):
                self.assertEqual(result[i * 10 + j].position, Vector2(i * 10, j * 10))


class MapBuilderLoadAssetsTest(unittest.TestCase):

    def setUp(self):
        self.map_builder = MapBuilder("src")

    def test_require_no_asset(self):
        map_source = json.dumps({
            "map": [],
            "background": ""
        })
        with patch("builtins.open", mock_open(read_data=map_source)):
            self.map_builder.construct_asset = Mock(return_value=None)
            self.map_builder.load_assets()
            self.assertEqual(len(self.map_builder.assets), 0)

    def test_load_all_assets(self):
        map_source = json.dumps({
            "assets": [
                {
                    "name": "brick",
                    "src": "brick.png"
                },
                {
                    "name": "ladder",
                    "src": "ladder.png"
                }
            ]
        })
        with patch("builtins.open", mock_open(read_data=map_source)):
            MapBuilder.construct_asset = Mock(return_value=None)
            self.map_builder.load_assets()
            self.assertEqual(len(self.map_builder.assets), 2)


class MapBuilderGetElementsTest(unittest.TestCase):

    def setUp(self):
        self.map_builder = MapBuilder("src")

    def test_require_no_map(self):
        map_source = json.dumps({
            "assets": [],
            "background": ""
        })
        with patch("builtins.open", mock_open(read_data=map_source)):
            self.map_builder.construct_object = Mock(return_value=None)
            self.map_builder.load_assets = Mock()
            self.map_builder.assets = []
            self.assertRaises(ValueError, self.map_builder.get_elements, None)

    def test_load_all_elements(self):
        map_source = json.dumps({
            "map": [
                {
                    "type": "rect",
                    "position": [1, 1],
                    "size": [10, 10]
                },
                {
                    "type": "rect",
                    "position": [2, 2],
                    "size": [12, 12]
                }
            ]
        })
        with patch("builtins.open", mock_open(read_data=map_source)):
            self.map_builder.construct_object = Mock(return_value=[None])
            self.map_builder.load_assets = Mock()
            self.map_builder.assets = []

            elements = self.map_builder.get_elements(None)
            self.assertEqual(len(elements), 2)
