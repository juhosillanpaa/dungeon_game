import pygame
from src.Utility.helpers.vector_helpers import calculate_angle
from ..Bullet.Bullet import Bullet
from ..MovingUnit.MovingUnit import MovingUnit
import numpy as np

W = 64
H = 64
WHITE = (255,255,255)
base = 'Classes/Cockroach/Cockroach_images/'

walking_path_list = [base+'cockroach.png', base+'cockroach_move1.png', base+'cockroach.png', base+'cockroach_move2.png']
attacking_path_list =[base + 'cockroach_attack1.png']
death_path_list = [base + 'cockroach_dead.png']

def get_image_matrix(width, height, path_list):
    arr = []
    for url in path_list:
        image = pygame.transform.scale(
            pygame.image.load(url),
            (width, height)
        )
        arr.append(image)
    return arr


class Cockroach(MovingUnit):
    def __init__(self, map):
        walk_animation_frames = get_image_matrix(96, 96, walking_path_list)
        super().__init__(height=96,
                         width=96,
                         velocity=1,
                         image=walk_animation_frames[0],
                         walk_animation_images=walk_animation_frames,
                         walk_animation_frame_duration=10,
                         attack_animation_images=get_image_matrix(96, 96, attacking_path_list),
                         attack_animation_frame_duration=20,
                         attack_interval=60,
                         death_animation_images=get_image_matrix(96,96,death_path_list),
                         death_animation_frame_duration=60,
                         norm_vector=(0, -1),
                         health=100,
                         map=map
                         )
        self.target = None
        self.scanRadius = 500
        self.attackRadius = 50
        self.hitbox_size = 20
        self.damage = 20


    def scan_for_target(self, hero):
        x, y = hero.get_position()
        distance = np.linalg.norm((x - self.x, y - self.y))
        if distance <= self.scanRadius:
            self.target = hero

    def update_facing_direction(self):
        if self.target is not None:
            x, y = self.target.get_position()
            super().update_facing_direction(x, y)

    def attack_if_off_cooldown(self):
        if super().is_attack_off_cooldown():
            super().attack(self.target, self.damage)
        else:
            pass

    def move_towards_target(self):
        if self.target is not None:
            x, y = self.target.get_position()
            path_dir_vec = (x - self.x, y - self.y)
            distance = np.linalg.norm(path_dir_vec)
            if distance < self.attackRadius:
                self.attack_if_off_cooldown()
                self.stop_moving()
            else:
                unit_dir_vec = path_dir_vec / distance
                x_delta = unit_dir_vec[0] * self.velocity
                y_delta = unit_dir_vec[1] * self.velocity
                if x_delta != 0 or y_delta != 0:
                    self.moving = True
                    super().set_position(self.x + x_delta, self.y + y_delta)
                else:
                    self.moving = False

    def get_hitbox_rect(self):
        offset = self.hitbox_size // 2
        rect = pygame.Rect(self.x - offset, self.y - offset, self.hitbox_size, self.hitbox_size)
        return rect


    def check_if_hit_by_bullets(self, hero):
        bullets = hero.get_bullets()
        rect = self.get_hitbox_rect()
        for bullet in bullets:
            if not bullet.has_collided() and rect.colliderect(bullet.get_rect()):
                bullet.collide()
                super().reduce_health(bullet.get_damage())



    def run_iteration(self, hero):
        if super().is_alive():
            self.check_if_hit_by_bullets(hero)
            self.scan_for_target(hero)
            self.update_facing_direction()
            self.move_towards_target()
        super().run_iteration()
