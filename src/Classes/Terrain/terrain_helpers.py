import math


def distance(a, b):
    return math.sqrt((a-b)**2)

def is_tile_wall(tile, print_tile=False):
    if tile[2] == 0:
        return True
    else:
        return False