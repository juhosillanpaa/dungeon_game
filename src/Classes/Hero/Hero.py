import pygame
from src.Utility.helpers.vector_helpers import calculate_angle
from ..Bullet.Bullet import Bullet
from ..MovingUnit.MovingUnit import MovingUnit
import numpy as np

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
    def __init__(self):
        walk_animation_frames = get_image_matrix(96, 96, walking_path_list)
        super().__init__(height=96,
                         width=96,
                         velocity=3,
                         image=walk_animation_frames[0],
                         walk_animation_images=walk_animation_frames,
                         walk_animation_frame_duration=20,
                         attack_animation_images=get_image_matrix(96,96,attacking_path_list),
                         attack_animation_frame_duration=20,
                         attack_interval=60,
                         death_animation_images=get_image_matrix(96,96,death_path_list),
                         death_animation_frame_duration=60,
                         norm_vector=(0, -1),
                         health=100
                         )
        self.bullets = []

    def listen_pressed_move_commands(self):
        keys = pygame.key.get_pressed()
        x = (keys[pygame.K_d] - keys[pygame.K_a]) * self.velocity
        y = (keys[pygame.K_s] - keys[pygame.K_w]) * self.velocity
        if x != 0 or y != 0:
            self.moving = True
            super().set_position(self.x + x, self.y + y)
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
        bullet_dir_vec = (x - self.x, y - self.y)
        unit_dir_vec = bullet_dir_vec / np.linalg.norm(bullet_dir_vec)
        bullet = Bullet(self.x, self.y, unit_dir_vec)
        self.bullets.append(bullet)

    def draw(self, game_surface, x_offset, y_offset):
        super().draw(game_surface, x_offset, y_offset)
        for bullet in self.bullets:
            bullet.draw(game_surface, x_offset, y_offset)


    def get_bullets(self):
        return self.bullets

    def get_position(self):
        return self.x, self.y