import numpy as np
import pandas as pd
from ..Map.WallTile import WallTile
from ..Map.FloorTile import FloorTile

import matplotlib.pyplot as plt
from perlin_noise import PerlinNoise



def test_perlin_map(size=50, tile_size = 128):

    noise = PerlinNoise(octaves=10, seed=1)
    xpix, ypix =100, 100
    pic = []
    for i in range(xpix):
        row = []
        for j in range(ypix):
            noise_val = noise([i / xpix, j / ypix])
            row.append(noise_val)
        pic.append(row)
    tile_map = []

    for x in range(size):
        row = []
        for y in range(size):
            point = pic[x][y]
            if -0.15 < point < 0.15:
                row.append(FloorTile(x=x * tile_size, y=y * tile_size, size=tile_size))
            else:
                row.append(WallTile(x=x * tile_size, y=y * tile_size, size=tile_size))
        tile_map.append(row)

    return tile_map




def create_map_matrix(size=20, tile_size = 128):
    matrix = np.zeros((size, size))
    for x in range(size):
        for y in range(size):
            if x == 0 or y == 0 or x == size - 1 or y == size - 1:
                matrix[x][y] = 1
    tile_map = []
    for x in range(size):
        row = []
        for y in range(size):
            point = matrix[x][y]
            if point == 0:
                row.append(FloorTile(x=x*tile_size, y=y*tile_size, size=tile_size))
            else:
                row.append(WallTile(x=x*tile_size, y=y*tile_size, size=tile_size))
        tile_map.append(row)

    return tile_map


