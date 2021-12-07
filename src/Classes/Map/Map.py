import numpy as np
import pygame
import math
from .create_map import create_map_matrix, test_perlin_map

class Map:
    def __init__(self, game_surface,tile_size=32):
        self.tile_map = test_perlin_map(100, tile_size=tile_size)
        self.game_surface = game_surface
        self.view_x = 0
        self.view_y = 0
        self.tile_size = tile_size



    def check_tile_for_collision(self, x, y):
        tile = self.get_tile(x, y)
        return tile.does_tile_collide_objects()

    def get_tile_size(self):
        return self.tile_size

    def get_map(self):
        return self.tile_map

    def draw(self, x_offset, y_offset):
        for row in self.tile_map:
            for item in row:
                item.draw(self.game_surface, x_offset, y_offset)


    def set_view_coordinates(self, x, y):
        self.view_x = x
        self.view_y = y

    def get_tile(self, x, y):
        row = math.floor(x / self.tile_size)
        column = math.floor(y // self.tile_size)
        tile = self.tile_map[row][column]
        return tile


    def test_circle_rect_collision(self, c_x, c_y, c_r, r_x, r_y, r_w, r_h):
        if c_x - c_r < r_x + r_w: #circle x starts before rect ends
            if c_y - c_r < r_y + r_h:   # circel y starts before rext y starts
                if c_x + c_r > r_x: #circle ends before rect starts
                    if c_y + c_r > r_y: #circle ends before rect starts
                        return True
        return False





    def get_tiles_inside_radius(self, x, y, r):
        s = self.tile_size
        tiles = []
        i = x - r
        while i < x + r + s:
            row = math.floor(i / s)
            j = y - r
            while j < y + r + s:
                column = math.floor(j / s)
                tile = self.tile_map[row][column]
                t_rect = tile.get_rect()
                if self.test_circle_rect_collision(
                        c_x=x, c_y=y, c_r=r,
                        r_x=t_rect[0], r_y=t_rect[1], r_w=t_rect[2], r_h=t_rect[3]):
                    tiles.append(tile)
                j += s
            i += s
        return tiles

    def is_position_walkable(self, x, y, r):
        tiles = self.get_tiles_inside_radius(x, y, r)
        for tile in tiles:
            if not tile.is_tile_walkable():
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
