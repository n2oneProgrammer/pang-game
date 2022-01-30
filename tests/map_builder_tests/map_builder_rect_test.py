import unittest

from pygame.math import Vector2

from models.map_builder import MapBuilder
from models.objects.rectangle import Rectangle


class MapBuilderConstructRectTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.map_builder = MapBuilder("src")

    # TYPE RECT
    def test_type_rect_require_no_color(self):
        map_object = {
            "type": "rect",
            "position": [0, 0],
            "size": [0, 0]
        }

        with self.assertRaises(ValueError):
            self.map_builder.construct_object(map_object, None)

    def test_type_rect_require_no_position(self):
        map_object = {
            "type": "rect",
            "color": "#000000",
            "size": [0, 0]
        }

        with self.assertRaises(ValueError):
            self.map_builder.construct_object(map_object, None)

    def test_type_rect_require_no_size(self):
        map_object = {
            "type": "rect",
            "color": "#000000",
            "position": [0, 0]
        }

        with self.assertRaises(ValueError):
            self.map_builder.construct_object(map_object, None)

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
            color="#123456",
            space=None
        )

        result = self.map_builder.construct_object(map_object, None)[0]
        self.assertIsInstance(result, Rectangle)
        self.assertEqual(result.position, expect.position)
        self.assertEqual(result.width, expect.width)
        self.assertEqual(result.height, expect.height)
        self.assertEqual(result.color, expect.color)
