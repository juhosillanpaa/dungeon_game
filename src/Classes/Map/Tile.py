import pygame
RED = (255,0,0)
GRAY = (100,100,100)

class Tile:
    def __init__(self, is_walkable, collide_objects, x, y, size):
        self.is_walkable = is_walkable
        self.collide_objects = collide_objects
        self.x = x
        self.y = y
        self.size = size
        self.highlight = 0
        self.evaluating = 0

    def does_tile_collide_objects(self):
        return self.collide_objects

    def is_tile_walkable(self):
        return self.is_walkable

    def get_rect(self):
        return self.x, self.y, self.size, self.size

    def highlight_tile(self, time):
        self.highlight = time

    def evaluate_tile(self, time):
        self.evaluating = time

    def get_center(self):
        return self.x + self.size // 2, self.y + self.size // 2


    def draw(self, game_surface, x_offset, y_offset, image):
        if self.highlight > 0:
            self.highlight -= 1
            pygame.draw.rect(game_surface, RED, (self.x - x_offset, self.y-y_offset, self.size, self.size))
        elif self.evaluating > 0:
            self.evaluating -= 1
            pygame.draw.rect(game_surface, GRAY, (self.x - x_offset + 1, self.y - y_offset +1, self.size-2, self.size-2))
        else:
            game_surface.blit(image, (self.x - x_offset, self.y - y_offset))