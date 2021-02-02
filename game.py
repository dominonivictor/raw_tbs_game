from collections import namedtuple
import misc.game_states as game_states
from player import Player
from map_objects.tile import Tile
from random import randint
import constants.colors as colors
import constants.globalish_constants as g_cons
from config import Config

from game_eye import GameEye
import functions.map_functions as map_funcs


class Game:
    def __init__(self, **kwargs):
        config = Config
        config.clean_players()
        self.state = game_states.START
        self.log = []
        self.event_list = []
        self.actors = []
        self.has_ended = False
        self.actors_num = kwargs.get("actors_num", g_cons.I_ACTORS_NUM)
        self.current_player = None

        self.p1 = config.p1
        self.p2 = config.p2
        self.players = [self.p1, self.p2]
        self.grid_size = kwargs.get("grid_size", 13)
        self.ini_spaces = kwargs.get("ini_spaces")
        # need to remember the diff from grid and board, i think board is the kv board
        self.t_coords = kwargs.get("t_coords", {})
        self.create_grid(grid_size=self.grid_size, t_coords=self.t_coords)

        self.board = kwargs.get("board")

        self.initial_setup()
        self.add_actors_to_init_tiles()

        game_eye = GameEye.instance()
        game_eye.set_game(self)

    def add_actors_to_init_tiles(self):
        p1_actors = [actor for actor in self.p1.actors]
        p2_actors = [actor for actor in self.p2.actors]
        self.actors.extend(p1_actors)
        self.actors.extend(p2_actors)
        # very ugly for now, but need to make a major refine on the apis
        for i, actor in enumerate(self.actors):
            try:
                self.add_actor_at_coord(actor, self.ini_spaces[i])
            except IndexError:
                break

    def create_grid(self, grid_size=13, t_coords={}):
        # TODO this is messy having to change the stuff in the middle of the process
        grid = []
        # use region here prob...
        for i in range(grid_size):
            row = []
            for j in range(grid_size):
                if not t_coords:  # random selected terrain
                    move_cost, tile_color = map_funcs.random_map_cost_tile_gen()
                else:
                    move_cost, tile_color = map_funcs.defined_map_cost_tile_gen(
                        x=j, y=i, t_coords=t_coords
                    )
                tile = Tile(move_cost=move_cost, color=tile_color)

                row.append(tile)
            grid.append(row)

        # this is very ugly... should it be here?
        grid = list(map(list, zip(*grid)))  # doing this to transpose

        self.grid = grid
        return grid

    def initial_setup(self, actors=[]):

        actors_num = self.actors_num

        players = [self.p1, self.p2]

        # actors_options()

        for player in players:
            self.create_actors(player, player.initial_actors)

    def create_actors(self, player, actors_list):
        from random import choice
        from misc.entities_creation import create_actor

        if type(actors_list) == str:
            for actor_letter in actors_list:
                player.add_actor(create_actor(actor_letter.lower(), self))
        else:
            for actor in actors_list:
                player.add_actor(actor)

    def add_actor_at_coord(self, actor, coord):
        x, y = coord
        # knows too much of grid!!!!!!!
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

    def check_win_condition(self):
        breakpoint()
        lost_players = []
        for player in self.players:
            dead_actors = 0
            for actor in player.actors:
                if actor.has_died:
                    dead_actors += 1
            if dead_actors == len(player.actors):
                lost_players.append(player)

        if lost_players:
            if len(lost_players) == 2:
                print("It's a draw")
            else:
                print(f"{lost_players[0].name} lost!")

            self.has_ended = True

        result_tuple = namedtuple("GameResult", ["has_ended", "lost_players"])
        result = result_tuple(self.has_ended, lost_players)
        return result
