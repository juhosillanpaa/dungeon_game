class Animation:
    def __init__(self, animation_images, frame_duration,loop=True):
        self.animation_images = animation_images
        self.frame_count = len(animation_images)
        self.frame_duration = frame_duration
        self.frame_counter = 0
        self.current_frame_idx = 0
        self.playing = False
        self.loop = loop

    def play(self):
        self.playing = True
        self.frame_counter = 0
        self.current_frame_idx = 0

    def stop(self):
        self.playing = False

    def get_current_frame(self):
        return self.animation_images[self.current_frame_idx]

    def run_iteration(self):
        self.frame_counter += 1
        if self.frame_counter >= self.frame_duration:
            self.current_frame_idx = (self.current_frame_idx + 1) % self.frame_count
            self.frame_counter = 0
            if not self.loop:
                self.playing = False

    def is_animation_playing(self):
        if self.playing:
            return True
        else:
            return False
