import misc.game_states as game_states
from player import Player
from map_objects.tile import Tile
from random import randint
import constants.colors as colors
import constants.globalish_constants as g_cons

from game_eye import GameEye
import functions.map_functions as map_funcs

class Game():
    def __init__(self, **kwargs):

        self.state = game_states.START
        self.log = []
        self.event_list = []
        self.actors = []
        self.actors_num = kwargs.get("actors_num", g_cons.I_ACTORS_NUM)
        self.p1 = Player(name='P1')
        self.grid_size = kwargs.get("grid_size", 13)
        self.ini_spaces = kwargs.get("ini_spaces", [])
        #need to remember the diff from grid and board, i think board is the kv board
        self.t_coords = kwargs.get("t_coords", {})
        self.create_grid(grid_size=self.grid_size,
                                     t_coords=self.t_coords)

        self.board = kwargs.get("board")

        self.initial_setup()
        self.add_actors_to_init_tiles()

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

    def add_actors_to_init_tiles(self):
        p1_actors = [actor for actor in self.p1.actors]
        self.actors.extend(p1_actors)
        #very ugly for now, but need to make a major refine on the apis 
        for i, actor in enumerate(self.actors):
            try:
                self.add_actor_at_coord(actor, self.ini_spaces[i])
            except IndexError:
                break

    def create_grid(self, grid_size=13, t_coords={}):
        #TODO this is messy having to change the stuff in the middle of the process
        grid = []
        #use region here prob...
        for i in range(grid_size):
            row = []
            for j in range(grid_size):
                if(not t_coords): #random selected terrain
                    move_cost, tile_color = map_funcs.random_map_cost_tile_gen()
                else:
                    move_cost, tile_color = map_funcs.defined_map_cost_tile_gen(
                                x=j, y=i, t_coords=t_coords)
                tile = Tile(move_cost=move_cost, color=tile_color)

                row.append(tile)
            grid.append(row)

        #this is very ugly... should it be here?
        grid = list(map(list, zip(*grid))) #doing this to transpose

        self.grid = grid
        return grid

    def initial_setup(self, actors=[]):

        actors_num = self.actors_num

        players = [self.p1]

        # actors_options()

        for player in players:
            self.select_initial_actor(player, actors_num if not
                                                actors else actors)

    def select_initial_actor(self, player, n_actors):
        from random import choice
        from misc.entities_creation import create_actor
        if type(n_actors) is not list:
            player_actors = []
            actors_l = ["t", "f", "c", "a", "p", "o"]

            #actors =  "".join([choice(actors_l) for _ in range(n_actors)]) #p_choice if p_choice else
            actors = "".join(actors_l)
            actors = list(actors[:n_actors])

            for actor in actors:
                player.add_actor(create_actor(actor, self))
        else:
            actors = n_actors

            for actor in actors:
                player.add_actor(actor)


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

    def get_tile(self, x, y):
        return self.grid[x][y]
