import numpy as np
import matplotlib.pyplot as plt
from opensimplex import OpenSimplex
from src.Classes.Map.WallTile import WallTile
from src.Classes.Map.FloorTile import FloorTile

FEATURE_SIZE = 12
FEATURE_SIZE_ENEMY = 6


def get_simplex_noise(x0, y0, x1, y1, tile_size):
    enemy_bit_map = get_simplex_noise_bitmap(x0, y0, x1, y1)
    enemies = []
    tmp = OpenSimplex(seed=1)
    bit_map = []
    tile_map = []
    for x in range(x0, x1):
        bit_row = []
        tile_row = []
        for y in range(y0, y1):
            n = tmp.noise2d(x=x / FEATURE_SIZE, y=y / FEATURE_SIZE)
            bit_row.append(n)
            if -0.2 < n < 0.6:
                tile = FloorTile(x=x * tile_size, y=y * tile_size, size=tile_size)
                if enemy_bit_map[x-x0][y-y0] > 0.7:
                    enemies.append((x*tile_size, y*tile_size))
            else:
                tile = WallTile(x=x * tile_size, y=y * tile_size, size=tile_size)
            tile_row.append(tile)
        bit_map.append(bit_row)
        tile_map.append(tile_row)
    matrix = np.asarray(tile_map)

    return matrix, enemies



def get_simplex_noise_bitmap(x0, y0, x1, y1):
    tmp = OpenSimplex(seed=2)
    bit_map = []


    for x in range(x0, x1):
        bit_row = []
        for y in range(y0, y1):
            n = tmp.noise2d(x=x / FEATURE_SIZE_ENEMY, y=y / FEATURE_SIZE_ENEMY)
            bit_row.append(n)

        bit_map.append(bit_row)
    matrix = np.asarray(bit_map)
    #plt.imshow(bit_map, cmap='gray')
    #plt.show()
    return matrix
