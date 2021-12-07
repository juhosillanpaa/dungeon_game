import pygame
import numpy as np
import math
from src.Utility.helpers.ray_casting import ray_cast

BLACK = (0, 0, 0)
GREY = (100,100,100)
BULLET_COLLISION_COLOR = (209, 80, 0)
MAX_DISTANCE = 96*100

class Bullet():
    def __init__(self, x, y, direction, collision_distance, damage=50):
        self.velocity = 10
        self.damage = damage
        self.start_x = x
        self.start_y = y
        self.x = x
        self.y = y
        self.direction = direction
        self.collision_distance = collision_distance
        self.collided = False
        self.collision_timer = 0
        self.distance_travelled = 0


    def update_position(self):
        if not self.collided:
            x_delta = self.direction[0] * self.velocity
            y_delta = self.direction[1] * self.velocity
            self.x += x_delta
            self.y += y_delta
            self.distance_travelled += math.sqrt(x_delta**2 + y_delta**2)
            if self.distance_travelled >= self.collision_distance:
                self.collided = True
                self.collision_timer = 30
                self.x = self.start_x + self.direction[0] * self.collision_distance
                self.y = self.start_y + self.direction[1] * self.collision_distance



    def draw(self, game_surface, x_offset, y_offset):
        bulletRect = pygame.Rect(self.x - x_offset -1, self.y - y_offset - 1, 3, 3)
        if game_surface.get_rect().contains(bulletRect):
            if self.collision_timer > 0:
                pygame.draw.rect(game_surface, BULLET_COLLISION_COLOR, bulletRect)
                self.collision_timer -= 1
            else:
                pygame.draw.rect(game_surface, BLACK, bulletRect)

    def get_rect(self):
        bulletRect = pygame.Rect(self.x, self.y, 3, 3)
        return bulletRect

    def collide(self):
        self.collided = True

    def has_collided(self):
        return self.collided

    def get_damage(self):
        return self.damage

    def should_be_removed_from_game(self):
        if (self.collided and self.collision_timer == 0) or self.distance_travelled > MAX_DISTANCE:
            return True
        else:
            return False
