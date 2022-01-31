import random
import pygame

wall = 'Classes/Map/MapTile_images/Wall_new.png'
floor = 'Classes/Map/MapTile_images/Floor_new.png'


class Tile:
    def __init__(self, game_surface, tile_size, image_url):
        self.game_surface = game_surface
        self.image = pygame.transform.scale(
            pygame.image.load(image_url), (tile_size, tile_size)
        )

    def draw(self, x, y):
        self.game_surface.blit(self.image, (x, y))


class Wall(Tile):
    def __init__(self, game_surface, tile_size=32):
        super().__init__(game_surface=game_surface, tile_size=tile_size, image_url=wall)


class Floor(Tile):
    def __init__(self, game_surface, tile_size=32):
        super().__init__(game_surface=game_surface, tile_size=tile_size, image_url=floor)




