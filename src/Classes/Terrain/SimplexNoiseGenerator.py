import numpy as np
from opensimplex import OpenSimplex
from src.Classes.Map.WallTile import WallTile
from src.Classes.Map.FloorTile import FloorTile
import matplotlib.pyplot as plt
from ..Spawn.spawn_helpers import pretest_is_valid_spawn_location

# Bit_map is a matrix representing the tile map, each cell is an array representing:
# [      0     ,       1     ,     2    ,   3
# [x_coordinate, y_coordinate, tile_type, enemy]
T_RATIO = 0.4
U_RATIO = 0.6

FLOOR = 1
WALL = 0

ROACH = 1
EMPTY = 0





def create_terrain_bitmap(x0, y0, x1, y1, featuresize=16, seed=1, featuresize2=32, seed2=2, tile_size=32):
    dist = featuresize * tile_size / 2
    path = OpenSimplex(seed=seed)
    area = OpenSimplex(seed=seed2)
    bit_map = []
    bit_map2 = []
    for x in range(x0, x1):
        bit_row = []
        bit_row2 = []
        for y in range(y0, y1):
            p = path.noise2d(x=x / featuresize, y=y / featuresize)
            a = area.noise2d(x= x / featuresize2, y=y / featuresize2)
            bit_row.append(p)
            bit_row2.append(a)
        bit_map.append(bit_row)
        bit_map2.append(bit_row2)

    bit_map3 = []
    spawn_locations = []
    for x in range(x0, x1):
        i = x - x0
        bit_row3 = []
        x_pos = x*tile_size
        for y in range(y0, y1):
            y_pos = y * tile_size
            j = y - y0
            if -0.3 < bit_map[i][j] < 0.3 or bit_map2[i][j] > 0.5 or bit_map2[i][j] < - 0.5:
                bit_row3.append([x * tile_size, y * tile_size, 1])
                if bit_map2[i][j] > 0.5 or bit_map2[i][j] < -0.5:
                    if pretest_is_valid_spawn_location((x_pos, y_pos), spawn_locations, dist):
                        spawn_locations.append([x_pos, y_pos, 2])

                elif -0.001 < bit_map[i][j] < 0.001:
                    if pretest_is_valid_spawn_location((x_pos, y_pos), spawn_locations, dist):
                        spawn_locations.append([x_pos, y_pos, 1])
            else:
                bit_row3.append([x_pos, y_pos, 0])
        bit_map3.append(bit_row3)

    arr = np.asarray(bit_map3)

    return arr, spawn_locations




