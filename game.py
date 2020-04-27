import misc.game_states as game_states
from menus import initial_setup
from player import Player
from map_objects.tile import Tile
from random import randint
import constants.colors as colors

class Game():
    def __init__(self, **kwargs):
        self.state = game_states.START
        self.log = []
        self.event_list = []
        self.actors = []
        self.initial_values = {
            "actors_num": 4,
            "jobs_num": 2,
            "equips_num": 2
        }
        self.p1 = Player(name='P1')
        self.p2 = Player(name='P2')
        self.grid_size = kwargs.get("grid_size", 13)
        self.grid = self.create_grid(grid_size=self.grid_size)

        self.board = kwargs.get("board")

        initial_setup(self.initial_values, p1=self.p1, p2=self.p2, game=self)
        self.add_actors()


    def show_actors(self):
        actor_str = ''
        i = 1
        for actor in self.actors:
            actor_str = actor_str + f'({i}) {actor.name}, '
            i += 1

        actor_str = actor_str[:-2] + '.'
        return actor_str

    def show_equipments(self):
        equip_str = ''
        i = 1
        for equip in self.equipments:
            equip_str = equip_str + f'({i}) {equip.name}, '
            i += 1

        equip_str = equip_str[:-2] + '.'
        return equip_str

    def add_actors(self):
        p1_actors = [actor for actor in self.p1.actors]
        p2_actors = [actor for actor in self.p2.actors]
        self.actors.extend(p1_actors)
        self.actors.extend(p2_actors)

    def create_grid(self, grid_size=13):
        grid = []
        for i in range(grid_size):
            row = []
            for j in range(grid_size):
                r = randint(1, 12)
                if r in [1, 2]:
                    move_cost = 2
                    tile_color = colors.FOREST_GREEN
                elif r in [3, 4]:
                    move_cost = 3
                    tile_color = colors.MOUNTAIN_ORANGE
                else:
                    move_cost = 1
                    tile_color = colors.BASIC_BLACK

                tile = Tile(move_cost=move_cost, color=tile_color)

                row.append(tile)
            grid.append(row)

        grid = list(map(list, zip(*grid))) #doing this to transpose
        return grid


