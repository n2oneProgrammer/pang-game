import math
import time

import pygame
import pymunk
from pygame import Surface
from pygame.math import Vector2

from models.enums.ColliderType import ColliderType
from models.enums.ObjectsCollisionType import ObjectCollisionType
from models.objects.chain_bullet import ChainBullet
from models.objects.sprite import Sprite
from models.utils.animation import Animation
from models.utils.sign import sign


class Player(Sprite):

    def __init__(self, position: Vector2, space, width=None, height=None,
                 velocity: Vector2 = Vector2(0, 0), collision_type=ColliderType.RECTANGLE, lives=5):

        from models.game_manager import GameManager
        if GameManager().player is None:
            GameManager().player = self

        self.player_lives = lives
        self.move_speed = 300
        self.time_shoot_animation = 0.3
        self.player_anim_walk_speed = 0.1
        self.player_anim_shoot_speed = 0.2
        self.gravity_speed = 200
        self.climbing_ladders = []
        self.blocking_objects = []
        self.move_direct = [0, 0]
        super().__init__("player_state/0.png", position, space, width, height, velocity, False, collision_type)
        self.body.elasticity = 1.0
        self.body.body_type = pymunk.Body.KINEMATIC
        shape = list(self.body.shapes)[0]
        shape.collision_type = ObjectCollisionType.PLAYER
        shape.filter = pymunk.ShapeFilter(categories=ObjectCollisionType.PLAYER,
                                          mask=pymunk.ShapeFilter.ALL_MASKS())

        self.animation_idle = Animation(
            self,
            ["player_state/0.png"],
            self.time_shoot_animation
        )

        self.animation_left = Animation(
            self,
            ["player_state/-1.png", "player_state/-2.png", "player_state/-3.png"],
            self.player_anim_walk_speed
        )

        self.animation_right = Animation(
            self,
            ["player_state/1.png", "player_state/2.png", "player_state/3.png"],
            self.player_anim_walk_speed
        )

        self.animation_shoot = Animation(
            self,
            ["player_state/bob-strzelanie.png"],
            self.player_anim_shoot_speed
        )

        self.last_shoot = 0

        move_collision_handler = space.add_collision_handler(ObjectCollisionType.PLAYER, ObjectCollisionType.WALL)
        move_collision_handler.begin = self.block_move_start
        move_collision_handler.separate = self.block_move_end

        move_collision_handler = space.add_collision_handler(ObjectCollisionType.PLAYER, ObjectCollisionType.LADDER)
        move_collision_handler.begin = self.add_climbing_ladder
        move_collision_handler.separate = self.remove_climbing_ladder

        ball_collision_handler = space.add_collision_handler(ObjectCollisionType.PLAYER, ObjectCollisionType.BALL)
        ball_collision_handler.begin = self.player_dead

    def run_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.move_direct[0] += -1
            if event.key == pygame.K_RIGHT:
                self.move_direct[0] += 1
            if event.key == pygame.K_UP:
                if len(self.climbing_ladders) > 0:
                    self.move_direct[1] += -1
            if event.key == pygame.K_DOWN:
                if len(self.climbing_ladders) > 0:
                    self.move_direct[1] += 1
            if event.key == pygame.K_SPACE:
                from models.game_manager import GameManager
                GameManager().scene.bullets.append(ChainBullet(self.position + Vector2(0, self.height), self.space))
                self.last_shoot = time.time()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                self.move_direct[0] += 1
            if event.key == pygame.K_RIGHT:
                self.move_direct[0] += -1
            if event.key == pygame.K_UP:
                if self.move_direct[1] < 0:
                    self.move_direct[1] += 1
            if event.key == pygame.K_DOWN:
                if self.move_direct[1] > 0:
                    self.move_direct[1] += -1

    def block_move(self):
        x_block = 0
        y_block = 0
        for element in self.blocking_objects:
            x_block += element[1][0]
            y_block += element[1][1]

        if x_block != 0 and self.body.velocity[0] / x_block > 0:
            self.velocity = Vector2(0, self.velocity.y)
        if y_block != 0 and self.body.velocity[1] / y_block > 0:
            self.velocity = Vector2(self.velocity.x, 0)

    def draw(self, screen: Surface):
        super().draw(screen)
        velocity = Vector2(0, 0)
        print(self.move_direct)
        velocity.x = sign(self.move_direct[0]) * self.move_speed
        velocity.y = sign(self.move_direct[1]) * 100 * sign(len(self.climbing_ladders))
        self.velocity = velocity
        if len(self.climbing_ladders) == 0 or (self.move_direct[1] == 0 and len(self.climbing_ladders) == 0):
            self.velocity = Vector2(self.velocity.x, self.gravity_speed)

        self.block_move()
        self.animation_controller()

    def animation_controller(self):
        if time.time() - self.last_shoot < self.time_shoot_animation:
            self.animation_shoot.change_enabled(True)
            self.animation_shoot.update()
        else:
            self.animation_left.change_enabled(self.velocity[0] < 0)
            self.animation_idle.change_enabled(self.velocity[0] == 0)
            self.animation_right.change_enabled(self.velocity[0] > 0)
            self.animation_left.update()
            self.animation_idle.update()
            self.animation_right.update()

    def block_move_start(self, data, space, other):
        for shape in data.shapes:
            if shape.collision_type == ObjectCollisionType.WALL:
                self.blocking_objects.append([shape, data.normal])

        return True

    def block_move_end(self, data, space, other):
        for shape in data.shapes:
            if shape.collision_type == ObjectCollisionType.WALL:
                temp = []
                for element in self.blocking_objects:
                    if element[0] != shape:
                        temp.append(element)

                self.blocking_objects = temp

        return True

    def add_climbing_ladder(self, data, space, other):
        for shape in data.shapes:
            if shape.collision_type == ObjectCollisionType.LADDER:
                self.climbing_ladders.append(shape)
        return False

    def remove_climbing_ladder(self, data, space, other):
        for shape in data.shapes:
            if shape.collision_type == ObjectCollisionType.LADDER:
                self.climbing_ladders.remove(shape)

        if len(self.climbing_ladders) == 0:
            self.velocity = Vector2(0, 0)

    def player_dead(self, data, space, other):
        self.player_lives -= 1
        print("You have ", self.player_lives)
        if self.player_lives <= 0:
            print("YOU DIED")

            from models.game_manager import GameManager
            GameManager().end_game()
        return False
