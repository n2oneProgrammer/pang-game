import math
import os.path
import unittest
from unittest.mock import Mock, MagicMock

import pymunk
from pygame.math import Vector2

from models.enums.ColliderType import ColliderType
from models.enums.ObjectsCollisionType import ObjectCollisionType
from models.objects.ball import Ball
from models.objects.sprite import Sprite


class BallTest(unittest.TestCase):
    def assumptions_test(self):
        Sprite.prepare_img = Mock()

        ball = Ball("test_img.png", Vector2(10, 20), None, 20)

        self.assertEqual(ball.width, 40)
        self.assertEqual(ball.height, 40)
        self.assertEqual(ball.collider_type, ColliderType.CIRCLE)
        self.assertEqual(list(ball.body.shapes)[0].collision_type, ObjectCollisionType.BALL)


class BallSplitTest(unittest.TestCase):
    def setUp(self):
        Sprite.prepare_img = Mock()

        self.space = pymunk.Space()
        self.space.gravity = 0, 100

        self.ball = Ball("test_img.png", Vector2(10, 20), self.space, 20, velocity=Vector2(100, -300))

        Ball.MIN_RADIUS = 10
        Ball.ANGLE_SPLIT_BALL = 60 * math.pi / 180
        Ball.PERCENT_LOSS_ENERGY = 3 / 10

    def delete_from_space_test(self):
        from models.game_manager import GameManager
        GameManager().scene = MagicMock()
        GameManager().scene.objects = [self.ball]
        self.ball.split()

        self.assertNotIn(self.ball.body, self.space.bodies)

    def delete_from_scene_test(self):
        from models.game_manager import GameManager
        GameManager().scene = MagicMock()
        GameManager().scene.objects = [self.ball]
        self.ball.split()

        self.assertNotIn(self.ball, GameManager().scene.objects)

    def create_small_balls_test(self):
        from models.game_manager import GameManager
        GameManager().scene = MagicMock()
        GameManager().scene.objects = [self.ball]
        self.ball.split()

        self.assertEqual(len(GameManager().scene.objects), 2)

    def position_small_balls_test(self):
        from models.game_manager import GameManager
        GameManager().scene = MagicMock()
        GameManager().scene.objects = [self.ball]
        self.ball.split()

        self.assertEqual(len(GameManager().scene.objects), 2)
        self.assertEqual(Vector2(0, 20), GameManager().scene.objects[0].position)
        self.assertEqual(Vector2(20, 20), GameManager().scene.objects[1].position)

    def image_path_small_balls_test(self):
        from models.game_manager import GameManager
        GameManager().scene = MagicMock()
        GameManager().scene.objects = [self.ball]
        self.ball.split()

        self.assertEqual(len(GameManager().scene.objects), 2)
        self.assertEqual(os.path.normpath("assets/test_img.png"), os.path.normpath(GameManager().scene.objects[0].path))
        self.assertEqual(os.path.normpath("assets/test_img.png"), os.path.normpath(GameManager().scene.objects[1].path))

    def radius_small_balls_test(self):
        from models.game_manager import GameManager
        GameManager().scene = MagicMock()
        GameManager().scene.objects = [self.ball]
        self.ball.split()

        self.assertEqual(len(GameManager().scene.objects), 2)
        self.assertEqual(20, GameManager().scene.objects[0].width)
        self.assertEqual(20, GameManager().scene.objects[1].width)

    def velocity_small_balls_test(self):
        from models.game_manager import GameManager
        GameManager().scene = MagicMock()
        GameManager().scene.objects = [self.ball]
        self.ball.split()

        self.assertEqual(len(GameManager().scene.objects), 2)
        self.assertAlmostEqual(-362.077, GameManager().scene.objects[0].velocity.x, 3)
        self.assertAlmostEqual(-209.045, GameManager().scene.objects[0].velocity.y, 3)
        self.assertAlmostEqual(362.077, GameManager().scene.objects[1].velocity.x, 3)
        self.assertAlmostEqual(-209.045, GameManager().scene.objects[1].velocity.y, 3)

    def stop_creating_small_balls_when_too_small_test(self):
        from models.game_manager import GameManager
        GameManager().scene = MagicMock()
        GameManager().scene.objects = [self.ball]
        self.ball.width = 20  # radius = 10
        self.ball.split()

        self.assertEqual(len(GameManager().scene.objects), 0)
