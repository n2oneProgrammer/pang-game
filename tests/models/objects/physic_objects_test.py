import unittest
from pygame.math import Vector2

from models.objects.physic_objects import PhysicObject


class PhysicObjectTest(unittest.TestCase):

    def test_check_assumption(self):
        physic_object = PhysicObject(Vector2(10, 10), None)
        self.assertEqual(physic_object.body.position, (10, 10))
        self.assertEqual(physic_object.body.velocity, (0, 0))

    def test_position_get(self):
        physic_object = PhysicObject(Vector2(10, 10), None)
        self.assertEqual(physic_object.position, Vector2(10, 10))

    def test_position_set(self):
        physic_object = PhysicObject(Vector2(10, 10), None)
        physic_object.position = Vector2(20, 20)
        self.assertEqual(physic_object.body.position, (20, 20))

    def test_velocity_get(self):
        physic_object = PhysicObject(Vector2(10, 10), None, velocity=Vector2(30, 10), is_static=False)
        self.assertEqual(physic_object.velocity, Vector2(30, 10))

    def test_velocity_set(self):
        physic_object = PhysicObject(Vector2(10, 10), None, velocity=Vector2(10, 20))
        physic_object.velocity = Vector2(20, 20)
        self.assertEqual(physic_object.body.velocity, (20, 20))
