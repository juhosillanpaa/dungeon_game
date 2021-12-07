import random
import pygame
wall1= 'Classes/Map/MapTile_images/Wall_new.png'
wall2= 'Classes/Map/MapTile_images/Wall_new.png'
from .Tile import Tile

def get_random_tile(size, rotate=False):
    r1 = random.random()
    r2 = random.random()
    url = wall1 if r1 <= 0.5 else wall2
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



class WallTile(Tile):
    def __init__(self,x , y, size):
        self.image = get_random_tile(size)
        super().__init__(is_walkable=False, collide_objects=True, x=x, y=y, size=size)

    def draw(self, game_surface, x_offset, y_offset):
        super().draw(game_surface, x_offset, y_offset, self.image)




