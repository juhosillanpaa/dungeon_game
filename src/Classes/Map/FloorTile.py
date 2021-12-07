import random
import pygame
from .Tile import Tile
floor1 = 'Classes/Map/MapTile_images/Floor_new.png'


def get_random_tile(size, rotate=False):
    r2 = random.random()
    url = floor1
    if rotate:
        if r2 < 0.25:
            rotation = 0
        elif r2 < 0.5:
            rotation = 90
        elif r2 < 0.75:
            rotation = 180
        else:
            rotation = 270
    else:
        rotation = 0
    image = pygame.transform.rotate(
        pygame.transform.scale(
            pygame.image.load(url), (size, size)
        ), rotation
    )
    return image


class FloorTile(Tile):
    def __init__(self, x, y, size):
        self.image = get_random_tile(size)
        super().__init__(is_walkable=True,collide_objects=False, x=x, y=y, size=size)

    def is_wall(self):
        return False

    def draw(self, game_surface, x_offset, y_offset):
        super().draw(game_surface, x_offset, y_offset, self.image)



