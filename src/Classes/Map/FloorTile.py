import random
import pygame
floor1 = 'Classes/Map/MapTile_images/floor1.png'


def get_random_tile(size):
    r2 = random.random()
    url = floor1
    if r2 < 0.25:
        rotation = 0
    elif r2 < 0.5:
        rotation = 90
    elif r2 < 0.75:
        rotation = 180
    else:
        rotation = 270
    image = pygame.transform.rotate(
        pygame.transform.scale(
            pygame.image.load(url), (size, size)
        ), rotation
    )
    return image


class FloorTile:
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size
        self.image = get_random_tile(size)

    def is_wall(self):
        return False

    def draw(self, game_surface, x_offset, y_offset):
        game_surface.blit(self.image, (self.x - x_offset, self.y - y_offset))


