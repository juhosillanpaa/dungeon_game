import math
import numpy as np
import pygame
import random
from ..Terrain.terrain_helpers import is_tile_wall

from ..Cockroach.Cockroach import Cockroach
from src.Utility.helpers.vector_helpers import distance
RADIUS = 32*30
ENEMY_COUNT = 2
RED = (255, 0, 0)
MAX_VIEW_D = 32 * 20

def get_random_offset():
    max_d = 32*3
    r1 = random.randrange(-max_d, max_d)
    r2 = random.randrange(-max_d, max_d)
    return r1, r2


class Spawn:
    def __init__(self, x, y, game, terrain, radius=RADIUS, enemy_count=ENEMY_COUNT):
        self.game = game
        self.terrain = terrain
        self.x = x
        self.y = y
        self.radius = radius
        self.cooldown_duration = 30*60
        self.cooldown = 0
        self.enemy_count = enemy_count
        self.enemies = []

    def get_location_and_radius(self):
        return self.x, self.y, self.radius

    def update_cooldown(self):
        all_dead = True
        for enemy in self.enemies:
            if enemy.is_alive():
                all_dead = False
        if self.cooldown > 0 and all_dead:
            self.cooldown -= 1

    def spawn_enemies(self):
        if distance((self.x, self.y), self.terrain.get_center_coordinates()) > MAX_VIEW_D:
            return
        if self.cooldown <= 0:
            ts = math.floor(self.game.get_tile_size() // 2)
            i = 0
            j = 0
            while i < self.enemy_count and j < self.enemy_count * 10:
                j += 1
                offset = get_random_offset()
                x, y = self.x + offset[0] + ts, self.y + offset[1] + ts
                if not is_tile_wall(self.terrain.get_tile_at_coordinates(x,y)):
                    # position is floor => can spawn enemy there
                    roach = Cockroach(map=self.game.get_map(), x=x, y=y)
                    self.game.add_roach(roach)
                    self.enemies.append(roach)
                    i += 1
            self.cooldown = self.cooldown_duration

    def run_iteration(self):
        self.update_cooldown()
        self.spawn_enemies()

    def draw(self):
        x_offset, y_offset = self.terrain.get_offset()
        surface = self.game.get_game_surface()
        tile_size = self.game.get_tile_size()
        x, y = self.x - x_offset, self.y - y_offset
        pygame.draw.rect(surface, RED, (x + 1, y + 1, tile_size - 2, tile_size - 2))
