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

import controllers.board_controller as board_con
import controllers.buttons_controller as btn_con

class LogScreen(BoxLayout):
    msg_list = []

class ScrollableLog(ScrollView):
    text = StringProperty('')

class StatsPanel(Label):
    rgba = ListProperty(colors.BASIC_BLACK)
    def update_actor_stats(self, actor):
        self.text = actor.show_battle_stats() if actor else "No actor selected"
        
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
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.grid_size = 13
        self.rows = 1
        self.grid = []
        self.graph = {}
        self.initial_spaces = [(2, 2), (6, 2), (10, 2), (2, 10), (2, 6), (10, 10), (6, 10), (10, 6)]
        self.highlighted_tiles = []
        board_con.board_clean_selected_things(board=self)
        self.game = Game(grid_size=self.grid_size, board=self)

    def create_grid(self):
        board_con.create_grid(board=self, size=self.grid_size)

    def select_tile(self, target_tile):
        board_con.select_tile(board=self, target_tile=target_tile)
                
    def pass_turn(self):
        board_con.pass_turn(board=self)


class GameApp(App):
    pass

if __name__ == '__main__':
    GameApp().run()
