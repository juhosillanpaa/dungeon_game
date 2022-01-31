import numpy as np
import pandas as pd
from ..Map.WallTile import WallTile
from ..Map.FloorTile import FloorTile
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
from perlin_noise import PerlinNoise

from opensimplex import OpenSimplex
from src.Utility.helpers.perlin_noise import PerlinNoiseGenerator


FEATURE_SIZE = 120

def get_simplex_noise(x0, y0, x1, y1, tile_size):
    tmp = OpenSimplex(seed=2)

    tile_map = []
    bit_map = []
    for x in range(x0, x1):
        row = []
        bit_row = []
        for y in range(y0, y1):
            n = tmp.noise2d(x=x / FEATURE_SIZE, y=y / FEATURE_SIZE)
            bit_row.append(n)
            if -0.3 < n < 0.3:
                row.append(FloorTile(x=x * tile_size, y=y * tile_size, size=tile_size))
            else:
                row.append(WallTile(x=x * tile_size, y=y * tile_size, size=tile_size))
        tile_map.append(row)
        bit_map.append(bit_row)

    plt.imshow(bit_map, cmap='gray')
    plt.show()

    numpy_arr = np.asarray(tile_map)
    return numpy_arr





def test_simplex(size=50, tile_size = 128):

    tile_map = []
    bit_map = []

    for i in range(size):
        row = []
        bit_row = []
        for j in range(size):
            n = tmp.noise2d(x=i/FEATURE_SIZE, y=j/FEATURE_SIZE)
            bit_row.append(n)
            if i == 0 or j == 0 or i == size - 1 or j == size - 1:
                row.append(WallTile(x=i * tile_size, y=j * tile_size, size=tile_size))

            elif -0.3 < n < 0.3:
                row.append(FloorTile(x=i * tile_size, y=j * tile_size, size=tile_size))
            else:
                row.append(WallTile(x=i * tile_size, y=j * tile_size, size=tile_size))
        tile_map.append(row)
        bit_map.append(bit_row)

    plt.imshow(bit_map, cmap='gray')
    plt.show()
    return tile_map





def test_own_perlin_generator(size=50, tile_size = 128):
    noise_generator = PerlinNoiseGenerator(2,6)
    tile_map = []
    bit_map = []
    for i in range(size):
        row = []
        bit_row = []
        for j in range(size):
            noise = noise_generator(i / size, j / size)
            bit_row.append(noise)
            if i == 0 or j == 0 or i == size - 1 or j == size - 1:
                row.append(WallTile(x=i * tile_size, y=j * tile_size, size=tile_size))

            elif -0.15 < noise < 0.15:
                row.append(FloorTile(x=i * tile_size, y=j * tile_size, size=tile_size))
            else:
                row.append(WallTile(x=i * tile_size, y=j * tile_size, size=tile_size))
        tile_map.append(row)
        bit_map.append(bit_row)

    plt.imshow(bit_map, cmap='gray')
    plt.show()
    return tile_map





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


