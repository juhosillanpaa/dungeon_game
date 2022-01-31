import pygame
from ..Map.Map import Map
from ..Hero.Hero import Hero
from ..Terrain.Terrain import Terrain
TILE_SIZE = 32
from ..Spawn.spawn_helpers import is_valid_spawn_location



class Game:
    def __init__(self, game_surface):
        self.tile_size = TILE_SIZE
        self.terrain = Terrain(game=self, game_surface=game_surface, tile_size=TILE_SIZE)
        self.map = Map(game=self, game_surface=game_surface, terrain=self.terrain, tile_size=TILE_SIZE)
        self.hero = Hero(map=self.map)
        self.roaches = []
        self.game_surface = game_surface
        self.spawns = []

    def get_game_surface(self):
        return self.game_surface

    def get_tile_size(self):
        return self.tile_size

    def get_map(self):
        return self.map

    def get_mouse_coordinates(self):
        x, y = pygame.mouse.get_pos()
        x_offset, y_offset = self.get_offset()
        x = x + x_offset
        y = y + y_offset
        return x, y

    def add_roach(self, cockroach):
        self.roaches.append(cockroach)

    def remove_rotten_roaches(self):
        alive = filter(lambda x: not x.should_be_removed_from_game(), self.roaches)
        self.roaches = list(alive)

    def run_iteration(self):
        x_offset, y_offset = self.get_offset()
        self.hero.run_iteration(x_offset, y_offset)
        hero_x, hero_y = self.hero.get_position()
        self.remove_rotten_roaches()
        self.terrain.run_iteration(x=hero_x, y=hero_y)
        for spawn in self.spawns:
            spawn.run_iteration()
        for roach in self.roaches:
            roach.run_iteration(self.hero)



    def get_offset(self):
        x, y = self.hero.get_position()
        x_offset = x - self.game_surface.get_width() // 2
        y_offset = y - self.game_surface.get_height() // 2
        return x_offset, y_offset

    def draw(self):
        x_offset, y_offset = self.get_offset()
        self.terrain.draw_terrain()
        for spawn in self.spawns:
            spawn.draw()

        for roach in self.roaches:
            roach.draw(self.game_surface, x_offset, y_offset)
        self.hero.draw(self.game_surface, x_offset, y_offset)

    def listen_mouse_presses(self, event):
        x_off, y_off = self.get_offset()
        self.hero.listen_mouse_presses(event, x_off, y_off)

    def update_map_coordinates(self):
        x, y = self.hero.get_position()
        self.map.set_view_coordinates(x, y)

    def add_spawn_if_valid(self, new_spawn):
        if is_valid_spawn_location(new_spawn=new_spawn, spawns=self.spawns):
            self.spawns.append(new_spawn)
