import numpy as np
import pygame
import math
import itertools
from .create_map import create_map_matrix, test_perlin_map, test_own_perlin_generator, test_simplex, get_simplex_noise
from src.Utility.helpers.SimplexNoiseGenerator import get_simplex_noise
from .map_helpers import test_joining
from ..Map.WallTile import WallTile
from ..Cockroach.Cockroach import Cockroach
from ..Terrain.terrain_helpers import is_tile_wall
CHUNK_SIZE = 30

LOAD_DISTANCE = 14


def test_circle_rect_collision(c_x, c_y, c_r, r_x, r_y, r_w, r_h):
    if c_x - c_r < r_x + r_w:  # circle x starts before rect ends
        if c_y - c_r < r_y + r_h:  # circle y starts before rext y starts
            if c_x + c_r > r_x:  # circle ends before rect starts
                if c_y + c_r > r_y:  # circle ends before rect starts
                    return True
    return False


class Map:
    def __init__(self, game, game_surface,terrain, tile_size=32 ):
        self.game = game
        self.terrain = terrain
        self.game_surface = game_surface
        self.view_x = 0
        self.view_y = 0
        self.tile_size = tile_size

    def check_tile_for_collision(self, x, y):
        tile = self.terrain.get_tile_at_coordinates(x, y)
        if is_tile_wall(tile):
            return True
        else:
            return False

    def get_tile_size(self):
        return self.tile_size

    def get_tile_rect(self, x, y):
        return self.terrain.get_tile_rect(x,y)

    def get_tiles_inside_radius(self, x, y, r):
        s = self.tile_size
        tiles = []
        i = x - r
        while i < x + r + s:
            j = y - r
            while j < y + r + s:
                tile = self.terrain.get_tile_rect(i, j)
                if test_circle_rect_collision(
                        c_x=x, c_y=y, c_r=r,
                        r_x=tile[0], r_y=tile[1], r_w=self.tile_size, r_h=self.tile_size):
                    tiles.append(tile)
                j += s
            i += s

        return tiles

    def is_position_walkable(self, x, y, r):
        tile_rects = self.get_tiles_inside_radius(x, y, r)
        for rect in tile_rects:
            tile = self.terrain.get_tile_at_coordinates(rect[0], rect[1])
            #self.terrain.evaluate_tile_at_coordinates(x=tile[0], y=tile[1], time=120)
            if is_tile_wall(tile, print_tile=True):
                return False
        return True

    def get_legal_movement_vec(self, current_pos, movement_vec, radius):

        x = current_pos[0] + movement_vec[0]
        y = current_pos[1] + movement_vec[1]
        if self.is_position_walkable(x, y, radius):
            return movement_vec
        elif self.is_position_walkable(x, current_pos[1], radius):
            return movement_vec[0], 0
        elif self.is_position_walkable(current_pos[0], y, radius):
            return 0, movement_vec[1]
        else:
            return 0, 0
