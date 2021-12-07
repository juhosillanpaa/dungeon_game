import pygame
from src.Utility.helpers.vector_helpers import calculate_angle
from ..Bullet.Bullet import Bullet
from ..MovingUnit.MovingUnit import MovingUnit
import numpy as np

from src.Utility.helpers.ray_casting import get_unit_direction_vec, ray_cast


W = 64
H = 64
WHITE = (255,255,255)
base = 'Classes/Hero/hero_images/'

walking_path_list = [base+'character_still.png', base+'character_moving1.png',
                     base+'character_still.png', base+'character_moving2.png']
attacking_path_list = [base+'character_still.png']
death_path_list = [base+'character_still.png']

def get_image_matrix(width, height, path_list):
    arr = []
    for url in path_list:
        image = pygame.transform.scale(
            pygame.image.load(url),
            (width, height)
        )
        arr.append(image)
    return arr


class Hero(MovingUnit):
    def __init__(self, map):
        walk_animation_frames = get_image_matrix(96, 96, walking_path_list)
        super().__init__(height=96,
                         width=96,
                         velocity=4,
                         image=walk_animation_frames[0],
                         walk_animation_images=walk_animation_frames,
                         walk_animation_frame_duration=20,
                         attack_animation_images=get_image_matrix(96,96,attacking_path_list),
                         attack_animation_frame_duration=20,
                         attack_interval=60,
                         death_animation_images=get_image_matrix(96,96,death_path_list),
                         death_animation_frame_duration=60,
                         norm_vector=(0, -1),
                         health=100,
                         map=map
                         )
        self.bullets = []

    def listen_pressed_move_commands(self):
        keys = pygame.key.get_pressed()
        dir_vec = (keys[pygame.K_d] - keys[pygame.K_a], keys[pygame.K_s] - keys[pygame.K_w])
        if dir_vec != (0, 0):
            unit_dir_vec = dir_vec / np.linalg.norm(dir_vec)
            x = unit_dir_vec[0] * self.velocity
            y = unit_dir_vec[1] * self.velocity
            if x != 0 or y != 0:
                self.moving = True
                super().set_position(self.x + x, self.y + y)
            else:
                self.moving = False
        else:
            self.moving = False


    def filter_bullets(self):
        alive_bullets = []
        for bullet in self.bullets:
            if not bullet.should_be_removed_from_game():
                alive_bullets.append(bullet)
        self.bullets = alive_bullets

    def run_iteration(self, x_offset=0, y_offset=0):
        self.listen_pressed_move_commands()
        self.update_facing_direction(x_offset, y_offset)
        self.filter_bullets()
        for bullet in self.bullets:
            bullet.update_position()
        super().run_iteration()




    def update_facing_direction(self, x_offset, y_offset):
        x, y = pygame.mouse.get_pos()
        super().update_facing_direction(x + x_offset, y + y_offset,)

    def listen_mouse_presses(self, event, x_offset, y_offset):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.shoot(x_offset, y_offset)

    def shoot(self, x_offset, y_offset):
        x, y = pygame.mouse.get_pos()
        x = x + x_offset
        y = y + y_offset
        collision_distance, unit_dir_vec, pos = ray_cast((self.x, self.y), (x, y), max_length=1000, map=self.map)
        print('collision_distance: ', collision_distance)
        bullet = Bullet(self.x, self.y, unit_dir_vec, collision_distance)
        self.bullets.append(bullet)

    def draw(self, game_surface, x_offset, y_offset):
        super().draw(game_surface, x_offset, y_offset)
        for bullet in self.bullets:
            bullet.draw(game_surface, x_offset, y_offset)

        self.draw_ray_cast(game_surface, x_offset, y_offset)

    def draw_ray_cast(self, game_surface, x_offset, y_offset):
        x, y = pygame.mouse.get_pos()
        x = x + x_offset
        y = y + y_offset
        length, unit_dir_vec, positions = ray_cast((self.x, self.y), (x, y), max_length=1000, map=self.map)

        end_pos = (self.x + unit_dir_vec[0]*length, self.y + unit_dir_vec[1]*length)
        surface_start = (self.x - x_offset, self.y-y_offset)
        surface_end = (end_pos[0] - x_offset, end_pos[1] - y_offset)
        BLACK = (0,0,0)
        RED = (255,0,0)
        GREEN = (0,255,0)

        pygame.draw.line(game_surface, BLACK, surface_start, surface_end, 2)
        for position in positions:
            surf_pos = (position[0] - x_offset, position[1] - y_offset)
            color = RED if position[2] == 1 else GREEN
            pygame.draw.circle(game_surface, color, surf_pos, 2)

    def get_bullets(self):
        return self.bullets

    def get_position(self):
        return self.x, self.y