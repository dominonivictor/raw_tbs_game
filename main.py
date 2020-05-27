from kivy.factory import Factory
from kivy.app import App
from kivy.properties import ListProperty, StringProperty
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView

from game import Game

import constants.colors as colors
import constants.globalish_constants as g_cons

import controllers.board_controller as board_con
import controllers.buttons_controller as btn_con
import controllers.log_controller as log_con

class LogScreen(BoxLayout):
    msg_list = []

class ScrollableLog(ScrollView):
    text = StringProperty('')

class StatsPanel(Label):
    rgba = ListProperty(colors.BASIC_BLACK)
    def update_actor_stats(self, actor):
        self.text = log_con.show_actor_stats(actor)

class MinorOptionsButton(Button):
    def on_press(self):
        btn_con.minor_btn_on_press(self)


class MinorOptionsBox(Factory.BoxLayout):
    commands_list = []
    def update_commands_list(self, commands_list):
        btn_con.minor_box_update_list(self, commands_list)

class MajorOptionsButton(Button):
    def on_press(self):
        btn_con.handle_major_options_btns(box=self)

class MajorOptionsBox(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        btn_con.gen_major_box_widgets(self)

class PuzzleTile(ButtonBehavior, Label):
    rgba = ListProperty([*colors.BASIC_BLACK])

class PuzzleGrid(Factory.GridLayout):
    #Is it having too many responsabilities?
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.grid_size = g_cons.GRID_SIZE
        self.rows = 1
        self.grid = []
        self.graph = {}
        self.initial_spaces = g_cons.INITIAL_SPACES
        self.highlighted_tiles = []
        board_con.board_clean_selected_things(board=self)

        #I don't think this should be here...
        self.game = Game(grid_size=self.grid_size, board=self,
                         ini_spaces=self.initial_spaces)

    def create_grid(self):
        board_con.create_grid(board=self, size=self.grid_size)

    def select_tile(self, target_tile):
        board_con.select_tile(board=self, target_tile=target_tile)

    def pass_turn(self):
        board_con.pass_turn(board=self)

    def set_selected_action(self, action_str):
        self.selected_action  = action_str


class GameApp(App):
    pass

if __name__ == '__main__':
    GameApp().run()
