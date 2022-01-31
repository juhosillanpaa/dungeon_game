import numpy as np
import pygame
import math
from ..Terrain.SimplexNoiseGenerator import create_terrain_bitmap
from ..Spawn.Spawn import Spawn
from ..Terrain.terrain_helpers import distance
from ..Terrain.TerrainTiles import Floor, Wall
from ..Spawn.Spawn import Spawn
SEED1 = 1
SEED2 = 2
F_SIZE1 = 32
F_SIZE2 = 64


LOAD_D = 16
REMOVE_D = 16
MAP_D = 14
BUFFER = 2

GRAY = (100,100,100)



class Terrain:
    def __init__(self, game, game_surface, tile_size=32):
        self.game = game
        self.tile_size = tile_size
        self.x = 0
        self.y = 0
        self.game_surface = game_surface
        bitmap, spawns = self.load_predefined_bitmap(-LOAD_D, -LOAD_D, LOAD_D, LOAD_D)
        self.terrain_bitmap = bitmap
        self.floorTile = Floor(game_surface=game_surface, tile_size=tile_size)
        self.wallTile = Wall(game_surface=game_surface, tile_size=tile_size)
        self.evaluating = []


# GETTERS
    def get_center_coordinates(self):
        return self.x, self.y

    def get_tile_rect(self, x, y):
        tile = self.get_tile_at_coordinates(x, y)
        return tile[0], tile[1], self.tile_size, self.tile_size

    def get_indexes_at_coordinates(self, x, y):
        return math.floor(x / self.tile_size), math.floor(y / self.tile_size)

    def get_tile_at_coordinates(self, x, y):
        x0, y0, x1, y1 = self.get_boundary_coordinates()
        row, column = self.get_bit_map_indexes_at_coordinates(x, y)
        if x0 <= x < x1 and y0 <= y < y1:
            tile = self.terrain_bitmap[row][column]
        else:
            # backup in case ray casting reaches to the edge of the loaded map
            tile = [x, y, 0]
        return tile

    def get_tile_type_at_coordinates(self, x, y):
        tile = self.get_tile_at_coordinates(x, y)
        return tile[2]

    def evaluate_tile_at_coordinates(self, x, y, time):
        tile = self.get_tile_at_coordinates(x, y)
        self.evaluating.append([tile[0], tile[1], time])


    def update_evaluation_timers(self):
        new_eval = []
        for item in self.evaluating:
            if item[2] > 0:
                new_eval.append([item[0], item[1], item[2] - 1])
        self.evaluating = new_eval

    def load_predefined_bitmap(self, x0, y0, x1, y1, featuresize=F_SIZE1, seed=SEED1, featuresize2=F_SIZE2,seed2=SEED2):
        return create_terrain_bitmap(x0, y0, x1, y1,
                                     featuresize=featuresize, seed=seed,
                                     featuresize2=featuresize2, seed2=seed2,
                                     tile_size=self.tile_size)

    def get_boundary_coordinates(self):
        top_left = self.terrain_bitmap[0][0]
        x0, y0 = top_left[0], top_left[1]
        shape = self.terrain_bitmap.shape
        bot_right = self.terrain_bitmap[shape[0] - 1][shape[1] - 1]
        x1, y1 = bot_right[0], bot_right[1]
        return x0, y0, x1, y1

    def get_boundary_indexes(self):
        top_left = self.terrain_bitmap[0][0]
        x0, y0 = self.get_indexes_at_coordinates(top_left[0], top_left[1])
        shape = self.terrain_bitmap.shape
        bot_right = self.terrain_bitmap[shape[0] - 1][shape[1] - 1]
        x1, y1 = self.get_indexes_at_coordinates(bot_right[0], bot_right[1])
        return x0, y0, x1 + 1, y1 + 1

    def update_center(self, x, y):
        self.x = x
        self.y = y

    def get_bit_map_indexes_at_coordinates(self, x, y):
        x0, y0, x1, y1 = self.get_boundary_coordinates()
        row = math.floor((x - x0) // self.tile_size)
        column = math.floor((y - y0) // self.tile_size)
        return row, column

    def get_offset(self):
        x_offset = self.x - self.game_surface.get_width() // 2
        y_offset = self.y - self.game_surface.get_height() // 2
        return x_offset, y_offset


    def set_terrain_bitmap(self, new_map):
        self.terrain_bitmap = new_map

    def run_iteration(self, x, y):
        # x, and y are the coordinates of the center of the screen
        self.update_center(x, y)
        self.load_bitmap_chunks()
        self.remove_old_bitmap_chunks()
        self.update_evaluation_timers()

    def create_spawns(self, new_spawns):
        if len(new_spawns) > 0:
            for item in new_spawns:
                c = 1 if item[2] == 1 else 3
                r = self.tile_size * 5 if item[2] == 1 else self.tile_size * 10
                spawn = Spawn(x=item[0], y=item[1], game=self.game, terrain=self, radius=r, enemy_count=c)
                self.game.add_spawn_if_valid(spawn)

    def load_bitmap_chunks(self):
        x, y = self.get_indexes_at_coordinates(x=self.x, y=self.y)
        x0, y0, x1, y1 = self.get_boundary_indexes()
        new_spawns = []
        if distance(x0, x) < LOAD_D:  # too close to left edge
            chunk, spawns = self.load_predefined_bitmap(x0=x0 - BUFFER, y0=y0, x1=x0, y1=y1)
            new_map = np.concatenate((chunk, self.terrain_bitmap,), axis=0)
            new_spawns.extend(spawns)
            self.set_terrain_bitmap(new_map)
            x0, y0, x1, y1 = self.get_boundary_indexes()

        if distance(x1, x) < LOAD_D:  # Too close to right edge
            chunk,spawns = self.load_predefined_bitmap(x0=x1, y0=y0, x1=x1 + BUFFER, y1=y1)
            new_map = np.concatenate((self.terrain_bitmap, chunk), axis=0)
            new_spawns.extend(spawns)
            self.set_terrain_bitmap(new_map)
            x0, y0, x1, y1 = self.get_boundary_indexes()

        if distance(y0, y) < LOAD_D:  # too close to top edge
            chunk,spawns = self.load_predefined_bitmap(x0=x0, y0=y0 - BUFFER, x1=x1, y1=y0)
            new_map = np.concatenate((chunk, self.terrain_bitmap), axis=1)
            new_spawns.extend(spawns)
            self.set_terrain_bitmap(new_map)
            x0, y0, x1, y1 = self.get_boundary_indexes()

        if distance(y1, y) < LOAD_D:  # Too close to bottom edge
            chunk, spawns = self.load_predefined_bitmap(x0=x0, y0=y1, x1=x1, y1=y1 + BUFFER)
            new_map = np.concatenate((self.terrain_bitmap, chunk), axis=1)
            new_spawns.extend(spawns)
            self.set_terrain_bitmap(new_map)
        self.create_spawns(new_spawns)


    def remove_old_bitmap_chunks(self):
        x, y = self.get_indexes_at_coordinates(x=self.x, y=self.y)
        x0, y0, x1, y1 = self.get_boundary_indexes()

        if distance(x0, x) > REMOVE_D:  # too far from left edge, delete first x rows
            new_map = np.delete(self.terrain_bitmap, 0, axis=0)
            self.set_terrain_bitmap(new_map)
            x0, y0, x1, y1 = self.get_boundary_indexes()

        if distance(x1, x) > REMOVE_D:  # Too far from right edge, delete last x rows
            new_map = np.delete(self.terrain_bitmap, -1, axis=0)
            self.set_terrain_bitmap(new_map)
            x0, y0, x1, y1 = self.get_boundary_indexes()

        if distance(y0, y) > REMOVE_D:  # too far from top edge, delete first column
            new_map = np.delete(self.terrain_bitmap, 0, axis=1)
            self.set_terrain_bitmap(new_map)
            x0, y0, x1, y1 = self.get_boundary_indexes()

        if distance(y1, y) > REMOVE_D:  # Too far from bottom edge, delete last column
            new_map = np.delete(self.terrain_bitmap, -1, axis=1)
            self.set_terrain_bitmap(new_map)

    def get_visible_bitmap(self):
        VD = 14     #how many tiles are at least visible from center to top/bottom/left/right
        x, y = self.get_indexes_at_coordinates(x=self.x, y=self.y)
        x0, y0, x1, y1 = self.get_boundary_indexes()
        i0, j0, i1, j1 = x - VD, y - VD,  x + VD, y + VD
        visible = []
        for i in range(i0, i1):
            x_index = i - x0
            row = []
            for j in range(j0, j1):
                y_index = j - y0
                row.append(self.terrain_bitmap[x_index][y_index])
            visible.append(row)

        return visible

    def draw_terrain(self):
        visible = self.get_visible_bitmap()
        x_offset, y_offset = self.get_offset()
        for row in visible:
            for point in row:
                x, y = point[0] - x_offset, point[1] - y_offset
                if point[2] == 1:
                    self.floorTile.draw(x=x, y=y)
                else:
                    self.wallTile.draw(x=x, y=y)
        self.draw_evaluated()

    def draw_evaluated(self):
        x_offset, y_offset = self.get_offset()
        for item in self.evaluating:
            x, y = item[0] - x_offset, item[1] - y_offset
            pygame.draw.rect(self.game_surface, GRAY,
                (x + 1, y + 1, self.tile_size - 2, self.tile_size - 2))

    def add_new_spawns_if_valid_locations(self, new_spawns):
        for spawn in new_spawns:
            self.game.add_spawn_if_valid(spawn)
