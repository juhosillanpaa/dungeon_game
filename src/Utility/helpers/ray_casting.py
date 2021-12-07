import math
import numpy as np


def length(dx, dy):
    return math.sqrt(dx**2 + dy**2)


def get_unit_direction_vec(pos1, pos2):
    dir_vec = (pos2[0] - pos1[0], pos2[1] - pos1[1])
    return dir_vec / np.linalg.norm(dir_vec)


def ray_cast(start_pos, dir_pos, max_length, map):
    positions = []
    start_rect = map.get_tile(start_pos[0], start_pos[1]).get_rect()
    unit_dir_vec = get_unit_direction_vec(start_pos, dir_pos)

    x_off = 0 if unit_dir_vec[0] >= 0 else -1
    y_off = 0 if unit_dir_vec[1] >= 0 else -1

    a_x = start_pos[0] - start_rect[0]
    a_y = start_pos[1] - start_rect[1]
    s = map.get_tile_size()

    if unit_dir_vec[0] > 0:
        mod_x = (s - a_x) / unit_dir_vec[0]
    elif unit_dir_vec[0] < 0:
        mod_x = a_x / unit_dir_vec[0]
    else:
        mod_x = math.inf

    if unit_dir_vec[1] > 0:
        mod_y = (s - a_y) / unit_dir_vec[1]
    elif unit_dir_vec[1] < 0:
        mod_y = a_y / unit_dir_vec[1]
    else:
        mod_y = math.inf


    c_x = 0
    c_y = 0
    while True:
        dx_x = unit_dir_vec[0] * mod_x if unit_dir_vec[0] != 0 else 0
        dy_x = unit_dir_vec[1] * mod_x if unit_dir_vec[1] != 0 else 0
        c_delta_x = length(dx_x, dy_x)

        dx_y = unit_dir_vec[0] * mod_y if unit_dir_vec[0] != 0 else 0
        dy_y = unit_dir_vec[1] * mod_y if unit_dir_vec[1] != 0 else 0
        c_delta_y = length(dx_y, dy_y)

        if c_x + c_delta_x < c_y + c_delta_y:
            c_x += c_delta_x
            current_pos = (start_pos[0] + unit_dir_vec[0]*c_x, start_pos[1] + unit_dir_vec[1]*c_x)
            positions.append((current_pos[0], current_pos[1], 1))
            mod_x = s / unit_dir_vec[0]

        else:
            c_y += c_delta_y
            current_pos = (start_pos[0] + unit_dir_vec[0] * c_y, start_pos[1] + unit_dir_vec[1] * c_y)
            positions.append((current_pos[0], current_pos[1], 2))
            mod_y = s / unit_dir_vec[1]
        tile = map.get_tile(current_pos[0] + x_off, current_pos[1] + y_off)
        if tile.does_tile_collide_objects():
            c_l = length(current_pos[0] + x_off - start_pos[0], current_pos[1]+y_off - start_pos[1])
            return c_l, unit_dir_vec, positions





