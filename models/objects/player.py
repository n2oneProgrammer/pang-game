import pygame
import pymunk
from pygame import Surface
from pygame.math import Vector2

from models.enums.ColliderType import ColliderType
from models.enums.ObjectsCollisionType import ObjectCollisionType
from models.objects.sprite import Sprite


class Player(Sprite):

    def __init__(self, path, position: Vector2, space, width=None, height=None,
                 velocity: Vector2 = Vector2(0, 0), collision_type=ColliderType.RECTANGLE):
        from models.game_manager import GameManager
        if GameManager().player is None:
            GameManager().player = self

        self.move_speed = 300

        super().__init__(path, position, space, width, height, velocity, False, collision_type)
        self.body.elasticity = 1.0
        self.body.body_type = pymunk.Body.KINEMATIC
        list(self.body.shapes)[0].collision_type = ObjectCollisionType.PLAYER
        self.normal_collision = 0, 0

        move_collision_handler = space.add_collision_handler(ObjectCollisionType.PLAYER, ObjectCollisionType.WALL)
        move_collision_handler.begin = self.block_move_start
        move_collision_handler.separate = self.block_move_end

        ball_collision_handler = space.add_collision_handler(ObjectCollisionType.PLAYER, ObjectCollisionType.BALL)
        ball_collision_handler.begin = self.player_dead

    def run_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.velocity = Vector2(-self.move_speed, 0)
            if event.key == pygame.K_RIGHT:
                self.velocity = Vector2(self.move_speed, 0)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                self.velocity = Vector2(0, 0)
            if event.key == pygame.K_RIGHT:
                self.velocity = Vector2(0, 0)

        self.block_move()

    def block_move(self):
        if (self.normal_collision[0] != 0 and self.body.velocity[0] / self.normal_collision[0] > 0) or (
            self.normal_collision[1] != 0 and self.body.velocity[1] / self.normal_collision[1] > 0):
            self.body.velocity = 0, 0

    def draw(self, screen: Surface):
        super().draw(screen)
        self.block_move()

    def block_move_start(self, data, space, other):
        self.normal_collision = data.normal

        return True

    def block_move_end(self, data, space, other):
        self.normal_collision = 0, 0
        return True

    @staticmethod
    def player_dead(data, space, other):
        from models.game_manager import GameManager
        GameManager().end_game()

        return True
