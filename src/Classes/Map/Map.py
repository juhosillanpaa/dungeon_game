import numpy as numpy
from .create_map import create_map_matrix, test_perlin_map

class Map:
    def __init__(self, game_surface,):
        self.tile_map = test_perlin_map(100, tile_size=32)
        self.game_surface = game_surface
        self.view_x = 0
        self.view_y = 0



    def get_map(self):
        return self.tile_map

    def draw(self, x_offset, y_offset):
        for row in self.tile_map:
            for item in row:
                item.draw(self.game_surface, x_offset, y_offset)


    def set_view_coordinates(self, x, y):
        self.view_x = x
        self.view_y = y

