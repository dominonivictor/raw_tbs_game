from kivy.factory import Factory
from kivy.app import App
from kivy.core.window import Window
from kivy.properties import (
    ListProperty,
    StringProperty,
    ObjectProperty,
    NumericProperty,
)
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.popup import Popup
from kivy.graphics.vertex_instructions import Line
from kivy.graphics.context_instructions import Color
from kivy.clock import Clock

from game import Game
from config import Config

import constants.colors as colors
import constants.globalish_constants as g_cons

import controllers.board_controller as board_con
import controllers.buttons_controller as btn_con
import controllers.log_controller as log_con

from time import sleep


class ScreenMaster(ScreenManager):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = App.get_running_app()
        self.app.screen_manager = self


def make_popup_btn():
    btn = Button(text="Exit Popup")
    pop = Popup(content=btn, auto_dismiss=True, size=(400, 400), size_hint=(None, None))
    btn.bind(on_release=pop.dismiss)
    return pop


class PopButton(Button):
    def on_release(self):
        self.make_popup_btn()

    def make_popup_btn(self):
        make_popup_btn()

class MainMenuScreen(Screen):
    main_menu_screen = ObjectProperty()
    pass

    def make_popup_btn(self):
        btn = Button(text="Cool Text")
        pop = Popup(
            content=btn, auto_dismiss=True, size=(400, 400), size_hint=(None, None)
        )
        btn.bind(on_release=self.start_game)
        pop.open()

    def start_game(self, *args):
        self.manager.current = "main_game_screen"

    def config(self, *args):
        self.manager.current = "player_config_screen"

#####################################################
############## GAME BOARD SCREEN ####################
#####################################################


class MainGameScreen(Screen):
    main_game_screen = ObjectProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(self._finish_init)

    def _finish_init(self, dt):
        app = App.get_running_app()
        for id_key, obj in self.ids.items():
            app.root.ids[id_key] = obj


#####################################################
############## PLAYER CONFIG SCREEN #################
#####################################################


class PlayerConfigScreen(Screen):
    player_config_screen = ObjectProperty()
    current_index = NumericProperty(0)
    actors = "foaptc".upper()
    current_player = Config.p1
    config = Config
    current_player_text = StringProperty("Current Player: P1")
    current_actors_text = ListProperty([*current_player.initial_actors,])
    buttons = []

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        app = App.get_running_app()
        app.player_config_screen = self

    def go_to_main_menu(self):
        self.manager.current = "main_menu_screen"

    def current_player_actor(self, index):
        return self.current_player.initial_actors[index]

    def cycle_actors(self, player_actor_index, btn):
        btn.current_index = (btn.current_index + 1) % len(self.actors)
        actor = self.actors[btn.current_index]
        self.current_player.replace_initial_actor_at_i(player_actor_index, actor)
        self.current_actors_text[player_actor_index] = actor

    def set_current_player(self, player_slug):
        self.current_player = eval(f"self.config.{player_slug}")
        self.current_player_text = f"Current Player: {player_slug.upper()}"
        self.current_actors_text = [*self.current_player.initial_actors]
        for actor, btn in zip(self.current_player.initial_actors, self.buttons):
            btn.current_index = self.actors.index(actor.upper())

    def print_debug(self):
        print(f"Config: {self.config.print_self()}")


class ActorChoiceButton(Button):
    text = StringProperty("initial_stuff")
    current_index = NumericProperty(0)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = App.get_running_app()
        self.app.player_config_screen.buttons.append(self)


class ActorConfigButton(Button):
    current_index = NumericProperty(0)


#####################################################
############## LOGS PANEL ###########################
#####################################################


class LogScreen(BoxLayout):
    msg_list = []


class ScrollableLog(ScrollView):
    text = StringProperty("")


#####################################################
############## STATS PANEL ##########################
#####################################################


class StatsPanel(Label):
    rgba = ListProperty(colors.BASIC_BLACK)

    def update_actor_stats(self, actor):
        self.text = log_con.show_actor_stats(actor)


#####################################################
############## MAIN BOARD - BOTTOM MENU #############
#####################################################


class CreateGridButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = App.get_running_app()
        self.app.create_grid_btn = self

    def on_release(self):
        app = self.app
        puzzle = app.puzzle
        t_coords = app.t_coords
        i_spaces = app.i_spaces
        actors = []
        puzzle.create_grid(t_coords=t_coords, i_spaces=i_spaces)


class MinorOptionsButton(Button):
    def on_release(self):
        btn_con.minor_btn_on_press(self)


class MinorOptionsBox(Factory.BoxLayout):
    commands_list = []

    def update_commands_list(self, commands_list):
        btn_con.minor_box_update_list(self, commands_list)


class MajorOptionsButton(Button):
    def on_release(self):
        btn_con.handle_major_options_btns(box=self)


class MajorOptionsBox(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        btn_con.gen_major_box_widgets(self)


#####################################################
################# MAIN BOARD ########################
#####################################################
class PuzzleTile(ButtonBehavior, Label):
    rgba = ListProperty([*colors.BASIC_BLACK])
    original_color = None
    last_color = None
    temp_color = None
    lines = []

    def add_line(self, line):
        self.add_widget(line)
        self.lines.append(line)

    def remove_lines(self):
        for line in self.lines:
            self.remove_line(line)

        self.lines = []

    def remove_line(self, line):
        self.remove_widget(line)

    def on_release(self):
        app = App.get_running_app()
        app.puzzle.select_tile(target_tile=self)

    def on_hover(self):
        board_con.tile_on_hover(self)

    def set_color(self, color):
        self.set_last_color(self.rgba)
        self.rgba = color

    def get_color(self):
        return self.rgba

    def set_last_color(self, color):
        if color != colors.AOE_PURPLE:
            self.last_color = color

    def get_last_color(self):
        return self.last_color

    def set_original_color(self, color):
        self.last_color = self.rgba
        self.original_color = color

    def get_original_color(self):
        return self.original_color

    def get_center_xy(self):
        return self.center_x, self.center_y


class PuzzleGrid(Factory.GridLayout):
    # Is it having too many responsabilities?
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = App.get_running_app()
        self.app.puzzle = self

        self.selected_command = None
        self.reset_hl_tiles()

        self.grid_size = self.app.grid_size
        # initial spaces
        self.i_spaces = self.app.i_spaces
        # target_coords
        self.t_coords = self.app.t_coords
        self.rows = 1
        self.grid = []
        self.graph = {}
        board_con.board_clean_selected_things(board=self)

        # I don't think this should be here...

        self.tiles_with_lines = []

    def start_game(self):
        self.game = Game(
            grid_size=self.grid_size,
            board=self,
            ini_spaces=self.i_spaces,
            t_coords=self.t_coords,
        )

    def add_line(self, target_tile, x0, y0, x1, y1):
        x0, y0, x1, y1 = int(x0), int(y0), int(x1), int(y1)
        line = MoveLine(x0=x0, y0=y0, x1=x1, y1=y1)
        # target_tile = self.grid[x1][y1]
        target_tile.add_line(line)
        self.tiles_with_lines.append(target_tile)

    def add_line_path(self, from_coord, to_coord):
        if to_coord == from_coord:
            return
        next_to_coord = self.movable_spaces[to_coord]["via"]
        x0, y0 = to_coord
        x1, y1 = next_to_coord
        target_real_xy = self.grid[x0][y0].get_center_xy()
        next_real_xy = self.grid[x1][y1].get_center_xy()
        self.add_line(*target_real_xy, *next_real_xy)
        self.add_line_path(from_coord, next_to_coord)

    def remove_lines(self):
        for tile in self.tiles_with_lines:
            tile.remove_lines()

    def reset_hl_tiles(self):
        self.temp_hl_tiles = []
        self.movable_hl_tiles = []
        self.attackable_hl_tiles = []
        self.hl_tiles = []

    def set_temp_hl_tiles(self, tiles):
        self.temp_hl_tiles = tiles

    def set_movable_hl_tiles(self, tiles):
        self.movable_hl_tiles = tiles

    def set_attackable_hl_tiles(self, tiles):
        self.attackable_hl_tiles = tiles

    def set_hl_tiles(self, tiles):
        self.hl_tiles = tiles

    def get_width(self):
        return len(self.grid)

    def get_height(self):
        return len(self.grid[0])

    def get_tile(self, x, y):
        return self.grid[x][y]

    def create_grid(self, t_coords={}, i_spaces=[]):
        self.start_game()
        board_con.create_grid(
            board=self,
            size=self.grid_size,
            t_coords=t_coords,
            i_spaces=i_spaces,
        )

    def select_tile(self, target_tile):
        board_con.select_tile(board=self, target_tile=target_tile)

    def pass_turn(self):
        board_con.pass_turn(board=self)

    def set_selected_action(self, action_str):
        self.selected_action = action_str

    def endgame_popup(self, lost_players):
        btn = Button(text=f"Player(s) Lost: {[p.name for p in lost_players]}")
        pop = Popup(
            content=btn, auto_dismiss=True, size=(400, 400), size_hint=(None, None), title="ENDGAME"
        )
        btn.bind(on_release=self.goto_main_menu)
        pop.open()
    
    def goto_main_menu(self, *args):
        self.app.screen_manager.current = 'main_menu_screen'

class MoveLine(Widget):
    def __init__(self, **kwargs):
        super().__init__()
        x0 = kwargs.get("x0")
        y0 = kwargs.get("y0")
        x1 = kwargs.get("x1")
        y1 = kwargs.get("y1")
        # print(f"VALUES: ({x0}, {y0}) ({x1}, {y1})")
        with self.canvas.before:
            Color(0, 0, 1, 1)
            Line(points=[x0, y0, x1, y1], width=2)


#####################################################
################# MAIN APP ##########################
#####################################################
class GameApp(App):
    def build(self):
        return ScreenMaster()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Window.bind(mouse_pos=self.on_mouse_pos)
        self.current_hover_tile = None
        self.last_hover_tile = None
        self.grid_size = kwargs.get("grid_size", g_cons.GRID_SIZE_BASE)
        self.i_spaces = kwargs.get("i_spaces", g_cons.I_SPACES_BASE)
        self.t_coords = kwargs.get("t_coords", g_cons.T_COORDS_RANDOM)

    def on_mouse_pos(self, window, pos):
        try:
            for row in self.root.ids.puzzle.grid:
                for tile in row:
                    if tile.collide_point(*pos):
                        self.current_hover_tile = tile
                        if self.current_hover_tile is not self.last_hover_tile:
                            self.last_hover_tile = tile
                            tile.on_hover()
        except AttributeError:
            pass


if __name__ == "__main__":
    GameApp().run()
