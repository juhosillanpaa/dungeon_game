import pygame
import numpy as np
import math

BLACK = (0, 0, 0)
MAX_DISTANCE = 96*100
class Bullet():
    def __init__(self, x, y, direction, damage=50):
        self.velocity = 10
        self.damage = damage
        self.x = x
        self.y = y
        self.direction = direction

        self.collided = False
        self.distance_travelled = 0

    def update_position(self):
        x_delta = self.direction[0] * self.velocity
        y_delta = self.direction[1] * self.velocity
        self.x += x_delta
        self.y += y_delta
        self.distance_travelled += math.floor(x_delta**2 + y_delta**2)


    def draw(self, game_surface, x_offset, y_offset):
        bulletRect = pygame.Rect(self.x - x_offset, self.y - y_offset, 3, 3)
        if game_surface.get_rect().contains(bulletRect):
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
        if self.collided or self.distance_travelled > MAX_DISTANCE:
            return True
        else:
            return False
