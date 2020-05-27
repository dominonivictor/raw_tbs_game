import misc.game_states as game_states
from player import Player
from map_objects.tile import Tile
from random import randint
import constants.colors as colors

from game_eye import GameEye

class Game():
    def __init__(self, **kwargs):

        self.state = game_states.START
        self.log = []
        self.event_list = []
        self.actors = []
        self.initial_values = kwargs.get("initial_values", {
            "actors_num": 3,
            "jobs_num": 2,
            "equips_num": 2
        })
        self.p1 = Player(name='P1')
        self.p2 = Player(name='P2')
        self.grid_size = kwargs.get("grid_size", 13)
        self.ini_spaces = kwargs.get("ini_spaces", [])
        #need to remember the diff from grid and board, i think board is the kv board
        self.grid = self.create_grid(grid_size=self.grid_size)

        self.board = kwargs.get("board")

        self.initial_setup()
        self.add_actors()

        game_eye = GameEye.instance()
        game_eye.set_game(self)

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
        #very ugly for now, but need to make a major refine on the apis 
        for i, actor in enumerate(self.actors):
            self.add_actor_at_coord(actor, self.ini_spaces[i])

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



    def initial_setup(self):

        actors_num = self.initial_values["actors_num"]
        jobs_num = self.initial_values["jobs_num"]
        equips_num = self.initial_values["equips_num"]

        players = [self.p1, self.p2]

        # actors_options()

        for player in players:
            self.select_initial_actor_job_equip(player, actors_num, jobs_num,
                                                equips_num)

    def select_initial_actor_job_equip(self, player, n_actors, n_jobs, n_equips):
        from random import choice
        from misc.entities_creation import create_actor
        player_actors = []
        player_equips = []
        player_jobs = []
        actors_l = ["t", "f", "c", "a", "p", "o"]
        jobs_l = ["g", "t", "c", "h", "m"]
        equips_l = ["z", "d", "c", "s"]

        #actors =  "".join([choice(actors_l) for _ in range(n_actors)]) #p_choice if p_choice else
        actors = "".join(actors_l)
        actors = list(actors[:n_actors])
        for actor in actors:
            player.add_actor(create_actor(actor, self))


    def add_actor_at_coord(self, actor, coord):
        x, y = coord
        #knows too much of grid!!!!!!!
        self.grid[x][y].actor = actor

    def pop_actor_at_coord(self, coord):
        x, y = coord
        tile = self.grid[x][y]
        actor = tile.actor
        tile.actor = None
        return actor

    def has_actor_on_xy(self, x, y):
        return bool(self.grid[x][y].actor)

