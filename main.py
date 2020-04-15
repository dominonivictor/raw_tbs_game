from kivy.factory import Factory
from kivy.app import App
from kivy.properties import ListProperty
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout

from game import Game

import constants.colors as colors

import controllers.grid_controller as grid_con
import controllers.buttons_controller as btn_con

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
        self.rows = 1
        self.grid = []
        self.initial_spaces = [(2, 2), (10, 2), (2, 10), (10, 10)]
        self.game = Game()
        grid_con.grid_clean_selected_things(grid_obj=self)

    def create_grid(self, size=13):
        grid_con.create_grid(grid_obj=self, size=size)

    # This is getting wayyyyyyyy too big... but after making stuff work minimally i'll look into
    # refactoring and removing stuff from here and putting in other files and stuff, here needs to be
    # clean functions that makes me understand what's happening
    def select_tile(self, target_tile):
        grid_con.select_tile(grid=self, target_tile=target_tile)
                
    def pass_turn(self):
        grid_con.pass_turn(grid_obj=self)


class GameApp(App):
    pass

if __name__ == '__main__':
    GameApp().run()
