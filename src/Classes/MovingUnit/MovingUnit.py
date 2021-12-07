import pygame
from src.Utility.helpers.vector_helpers import calculate_angle
from ..Animation.Animation import Animation
from ..Attack.Attack import Attack
from ..HealthBar.HealthBar import HealthBar

UPDATE_FRAME=20

GREEN = (0, 255, 0)
HEALTH_BAR_WIDTH = 60
RADIUS = 15

class MovingUnit:
    def __init__(self, height, width, velocity,norm_vector, health, image,
                 walk_animation_images, walk_animation_frame_duration,
                 attack_animation_images, attack_animation_frame_duration, attack_interval,
                 death_animation_images, death_animation_frame_duration,
                 map
                 ):
        self.x = 0
        self.y = 0
        self.width = width
        self.height = height
        self.velocity = velocity

        self.rotation = 0
        self.norm_vector = norm_vector
        self.health = health
        self.image = image
        self.walk_animation = Animation(
            animation_images=walk_animation_images,
            frame_duration=walk_animation_frame_duration
        )
        self.death_animation = Animation(
            animation_images=death_animation_images,
            frame_duration=death_animation_frame_duration,
            loop=False
        )
        self.moving = False
        self.attack = Attack(
            attack_interval=attack_interval,
            animation_images=attack_animation_images,
            frame_duration=attack_animation_frame_duration
        )
        self.health_bar = HealthBar(0, 0, health, HEALTH_BAR_WIDTH)
        self.map = map



    def get_animation_frame(self):
        if not self.is_alive():
            image = self.death_animation.get_current_frame()
        elif self.attack.is_animation_playing():
            image = self.attack.get_animation_frame()
        elif self.moving:
            image = self.walk_animation.get_current_frame()
        else:
            image = self.image
        return image

    def run_iteration(self):
        if not self.is_alive():
            self.death_animation.run_iteration()
        else:
            if self.moving:
                self.walk_animation.run_iteration()
            if self.attack.attacking:
                self.attack.run_iteration()


    def draw(self, game_surface, x_offset, y_offset):
        if self.is_alive():
            self.health_bar.draw(game_surface, self.health, x_offset, y_offset)
        image = self.get_animation_frame()
        rotated_img = pygame.transform.rotate(image, self.rotation)
        x = self.x - rotated_img.get_width() // 2 - x_offset
        y = self.y - rotated_img.get_height() // 2 - y_offset
        pygame.draw.circle(game_surface, GREEN, (self.x - x_offset, self.y-y_offset), RADIUS)
        game_surface.blit(rotated_img, (x, y))


    def update_facing_direction(self, x, y):
        new_dir = (x - self.x, y - self.y)
        rot = calculate_angle(self.norm_vector, new_dir)
        self.rotation = rot

    def get_position(self):
        return self.x, self.y

    def set_position(self, x, y):
        current_pos = (self.x, self.y)
        movement_vec = (x - self.x, y - self.y)
        legal_mov_vec = self.map.get_legal_movement_vec(current_pos, movement_vec, RADIUS)
        x = self.x + legal_mov_vec[0]
        y = self.y + legal_mov_vec[1]
        self.x = x
        self.y = y
        hp_x = self.x - HEALTH_BAR_WIDTH // 2
        hp_y = self.y - self.height // 2
        self.health_bar.update_position(hp_x, hp_y)


    def start_moving(self):
        self.moving = True

    def stop_moving(self):
        self.moving = False

    def reduce_health(self, dmg):
        self.health -= dmg
        if self.health <= 0:
            self.death_animation.play()

    def is_attack_off_cooldown(self):
        return self.attack.is_attack_off_cooldown()

    def attack(self, target, damage):
        self.attack.attack()
        target.reduce_health(damage)

    def get_rect(self):
        x = self.x - self.width // 2
        y = self.y - self.height // 2
        rect = pygame.Rect(x, y, self.width, self.height)
        return rect

    def is_alive(self):
        if self.health > 0:
            return True
        else:
            return False

    def should_be_removed_from_game(self):
        if self.health <= 0 and not self.death_animation.is_animation_playing():
            return True
        else:
            return False