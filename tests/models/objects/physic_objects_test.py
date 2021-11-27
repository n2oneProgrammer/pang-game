import unittest
from parameterized import parameterized
from pygame.math import Vector2

from models.objects.physic_objects import PhysicObject


class PhysicObjectTest(unittest.TestCase):

    def test_check_assumption(self):
        physic_object = PhysicObject([10, 10])
        self.assertEqual(physic_object.position, [10, 10])
        self.assertEqual(physic_object.velocity, [0, 0])
        self.assertEqual(physic_object.acceleration, [0, 0])
        self.assertEqual(physic_object.is_static, False)

    @parameterized.expand([
        ("0 velocity", (10, -80), (0, 0), (10, -80)),
        ("x velocity", (10, -80), (20, 0), (30, -80)),
        ("y velocity", (10, -80), (0, 20), (10, -60)),
        ("x,y velocity", (10, -80), (20, 20), (30, -60))
    ])
    def test_calc_position(self, name, start_position, velocity, expected_position):
        physic_object = PhysicObject(Vector2(start_position), Vector2(velocity))
        physic_object.calc_position(1)
        self.assertEqual(physic_object.position, Vector2(expected_position))

    def test_check_not_changing_position_when_is_static(self):
        physic_object = PhysicObject(Vector2(10, 10), Vector2(20, 20), is_static=True)
        physic_object.calc_position(1)
        self.assertEqual(physic_object.position, [10, 10])

    @parameterized.expand([
        ("0 acceleration", (10, -80), (0, 0), (10, -80)),
        ("x acceleration", (10, -80), (20, 0), (30, -80)),
        ("y acceleration", (10, -80), (0, 20), (10, -60)),
        ("x,y acceleration", (10, -80), (20, 20), (30, -60))
    ])
    def test_calc_velocity(self, name, start_velocity, acceleration, expected_velocity):
        physic_object = PhysicObject(Vector2(0, 0), Vector2(start_velocity), Vector2(acceleration))
        physic_object.calc_velocity(1)
        self.assertEqual(physic_object.velocity, Vector2(expected_velocity))

    def test_check_not_changing_velocity_when_is_static(self):
        physic_object = PhysicObject(Vector2(10, 10), Vector2(20, 20), is_static=True)
        physic_object.calc_velocity(1)
        self.assertEqual(physic_object.velocity, Vector2(20, 20))
