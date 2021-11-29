

class Game:
    def __init__(self, hero, game_surface, map):
        self.hero = hero
        self.roaches = []
        self.game_surface = game_surface
        self.map = map


    def add_roach(self, cockroach):
        self.roaches.append(cockroach)

    def remove_rotten_roaches(self):
        alive = filter(lambda x: not x.should_be_removed_from_game(), self.roaches)
        self.roaches = list(alive)

    def run_iteration(self):
        x_offset, y_offset = self.get_offset()
        self.hero.run_iteration( x_offset, y_offset)
        self.remove_rotten_roaches()
        for roach in self.roaches:
            roach.run_iteration(self.hero)


    def get_offset(self):
        x, y = self.hero.get_position()
        x_offset = x - self.game_surface.get_width() // 2
        y_offset = y - self.game_surface.get_height() // 2
        return x_offset, y_offset

    def draw(self):
        x_offset, y_offset = self.get_offset()
        self.map.draw(x_offset, y_offset)
        for roach in self.roaches:
            roach.draw(self.game_surface, x_offset, y_offset)
        self.hero.draw(self.game_surface, x_offset, y_offset)

    def listen_mouse_presses(self, event):
        x_off, y_off = self.get_offset()
        self.hero.listen_mouse_presses(event, x_off, y_off)

    def update_map_coordinates(self):
        x, y = self.hero.get_position()
        self.map.set_view_coordinates(x, y)
