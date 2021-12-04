import os
import unittest
from unittest.mock import Mock

from models.map_builder import MapBuilder


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
