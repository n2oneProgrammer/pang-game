import json
import os
import unittest
from unittest.mock import Mock, patch, mock_open, MagicMock

import pygame.image
from pygame.math import Vector2

from models.map_builder import MapBuilder
from models.objects.physic_objects import PhysicObject
from models.objects.player import Player
from models.objects.sprite import Sprite


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

    def test_require_no_player(self):
        map_source = json.dumps({
            "assets": [],
            "background": "",
            "map": []
        })
        with patch("builtins.open", mock_open(read_data=map_source)):
            self.map_builder.construct_object = Mock(return_value=None)
            self.map_builder.load_assets = Mock()
            self.map_builder.assets = []
            self.assertRaises(ValueError, self.map_builder.get_elements, None)

    def test_require_no_start_position_in_player(self):
        map_source = json.dumps({
            "assets": [],
            "background": "",
            "map": [],
            "player": {
                "lives": 5
            }
        })
        with patch("builtins.open", mock_open(read_data=map_source)):
            self.map_builder.construct_object = Mock(return_value=None)
            self.map_builder.load_assets = Mock()
            self.map_builder.assets = []
            self.assertRaises(ValueError, self.map_builder.get_elements, None)

    def test_require_no_lives_in_player(self):
        map_source = json.dumps({
            "assets": [],
            "background": "",
            "map": [],
            "player": {
                "start_position": [0, 0]
            }
        })
        with patch("builtins.open", mock_open(read_data=map_source)):
            self.map_builder.construct_object = Mock(return_value=None)
            self.map_builder.load_assets = Mock()
            self.map_builder.assets = []
            self.assertRaises(ValueError, self.map_builder.get_elements, None)

    def test_create_player(self):
        map_source = json.dumps({
            "assets": [],
            "background": "",
            "map": [],
            "player": {
                "start_position": [10, 20],
                "lives": 4
            }
        })
        with patch("builtins.open", mock_open(read_data=map_source)):
            self.map_builder.construct_object = Mock(return_value=None)
            self.map_builder.load_assets = Mock()
            self.map_builder.assets = []

            def prepare_img(self):
                self.width = 50

            Sprite.prepare_img = prepare_img
            space = MagicMock()
            space.add_collision_handle = MagicMock()
            elements = self.map_builder.get_elements(space)

            self.assertEqual(len(elements), 1)
            player = elements[0]
            self.assertIsInstance(player, Player)
            self.assertEqual(player.player_lives, 4)
            self.assertEqual(player.position.x, 10)
            self.assertEqual(player.position.y, 20)

    def test_load_background_solid_color(self):
        map_source = json.dumps({
            "assets": [],
            "background": "#111111"
        })
        with patch("builtins.open", mock_open(read_data=map_source)):
            self.map_builder.load_background()

            self.assertEqual(self.map_builder.background_color, "#111111")
            self.assertEqual(self.map_builder.background_image, None)

    def test_load_background_img(self):
        map_source = json.dumps({
            "assets": [],
            "background": "background.png"
        })
        with patch("builtins.open", mock_open(read_data=map_source)):
            pygame.image.load = Mock()
            pygame.transform.scale = Mock(return_value="image")

            self.map_builder.load_background()

            self.assertEqual(self.map_builder.background_color, None)
            self.assertEqual(self.map_builder.background_image, "image")

    def test_load_all_elements(self):
        map_source = json.dumps({
            "player": {
                "start_position": [0, 0],
                "lives": 5
            },
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

            space = MagicMock()
            space.add_collision_handle = MagicMock()
            elements = self.map_builder.get_elements(space)
            self.assertEqual(len(elements), 3)
