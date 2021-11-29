from ..Animation.Animation import Animation


class Attack:
    def __init__(self, attack_interval, animation_images, frame_duration):
        self.attack_interval = attack_interval
        self.cooldown_counter = 0
        self.animation_length = len(animation_images) * frame_duration
        self.animation = Animation(animation_images, frame_duration)
        self.attacking = False          # true if during attack or attack on cooldown

    def is_attack_off_cooldown(self):
        if self.cooldown_counter == 0:
            return True
        else:
            return False

    def attack(self):
        self.attacking = True
        self.animation.play()

    def run_iteration(self):
        if self.attacking:
            self.cooldown_counter += 1
            self.animation.run_iteration()
            if self.cooldown_counter == self.animation_length:
                self.animation.stop()
            if self.cooldown_counter == self.attack_interval:
                self.cooldown_counter = 0
                self.attacking = False

    def is_animation_playing(self):
        return self.animation.is_animation_playing()

    def get_animation_frame(self):
        return self.animation.get_current_frame()


