from kivy.base import runTouchApp
from kivy.lang import Builder
from kivy.factory import Factory
from kivy.app import App
from kivy.properties import ListProperty
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout

from game import Game
import misc.game_states as gs

import constants.colors as colors


class StatsPanel(Label):
    rgba = ListProperty(colors.BASIC_BLACK)
    def update_actor_stats(self, actor):
        self.text = actor.show_battle_stats() if actor else "No actor selected"
        
class MinorOptionsButton(Button):
    def on_press(self):
        app = App.get_running_app()
        app.root.ids.puzzle.selected_action = "command"
        app.root.ids.puzzle.selected_command = self.command
        app.root.ids.puzzle.state = gs.TARGETING

class MinorOptionsBox(Factory.BoxLayout):
    commands_list = []
    def update_commands(self, actor_commands_list):
        if not actor_commands_list: 
            self.commands_list = []
            self.clear_widgets()
        else:
            self.commands_list = []
            self.clear_widgets()
            command_btn = Factory.MinorOptionsButton
            for command in actor_commands_list:
                btn = command_btn(text=command.name)
                btn.command = command
                self.add_widget(btn)
                self.commands_list.append(command)


class MajorOptionsButton(Button):
    def on_press(self):
        if self.text == 'move':
            app = App.get_running_app()
            grid = app.root.ids.puzzle 

            if grid.selected_tile.actor:
                grid.state = gs.TARGETING
                grid.selected_action = "move"
                print("targeting mode")
            else:
                print("No actor selected")
        else:
            print("another button with no on_press func yet")


class MajorOptionsBox(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.buttons_list = [
            MajorOptionsButton(text="move"),
            MajorOptionsButton(text="learn job"),
            MajorOptionsButton(text="equip weapon"),
        ]
        for btn in self.buttons_list:
            self.add_widget(btn)

class PuzzleTile(ButtonBehavior, Label):
    rgba = ListProperty([*colors.BASIC_BLACK])

class PuzzleGrid(Factory.GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.rows = 1
        self.grid = []
        self.initial_spaces = [(2, 2), (10, 2), (2, 10), (10, 10)]
        self.game = Game()
        self.clean_selecteds()

    def clean_selecteds(self):
        self.selected_tile = None
        self.selected_action = None
        self.selected_command = None
        #self.target_tile = None
        self.state = gs.NORMAL

    def set_size(self, size=13):

        self.grid = []
        self.clear_widgets()
        try:
            self.rows = int(size)
            self.cols = int(size)
        except ValueError:
            return

        #making the grid
        PT = Factory.PuzzleTile
        for i in range(self.rows):
            grid_cols = []
            for j in range(self.cols):
                tile = PT(text=f'.')
                tile.actor = None
                tile.grid_x, tile.grid_y = i, j
                self.add_widget(tile)
                grid_cols.append(tile)

            self.grid.append(grid_cols)

        #adding actors initially
        for i, (x, y) in enumerate(self.initial_spaces):
            tile = self.grid[x][y]
            actor = self.game.actors[i]
            tile.text = actor.name[0]
            tile.actor = actor
            actor.update_pos(x=x, y=y)

    # This is getting wayyyyyyyy too big... but after making stuff work minimally i'll look into
    # refactoring and removing stuff from here and putting in other files and stuff, here needs to be
    # clean functions that makes me understand what's happening
    def select_tile(self, target_tile):
        app = App.get_running_app()
        if self.state == gs.NORMAL:
            if self.selected_tile:
                self.selected_tile.rgba = colors.BASIC_BLACK

            target_tile.rgba = colors.SELECTED_RED
            self.selected_tile = target_tile
            actor = target_tile.actor if target_tile.actor else None
            actor_command_list = actor.commands.list if actor else []
        
            app.root.ids.stats_panel.update_actor_stats(actor)
            app.root.ids.minor_options.update_commands(actor_command_list)

        elif self.state == gs.TARGETING:
            if not self.selected_tile.actor:
                print("no actor selected!")
                self.state = gs.NORMAL
            else:
                current_tile = self.selected_tile
                actor = current_tile.actor

                if self.selected_action == "move":
                    # import pdb; pdb.set_trace()
                    if actor.has_moved:
                        print("actor has already moved!")
                    elif target_tile.actor:
                        print("This tile is already ocuppied!")
                    else:
                        target_tile.actor = actor
                        current_tile.rgba = colors.BASIC_BLACK
                        current_tile.text = "."
                        target_tile.text = target_tile.actor.name[0]
                        target_tile.rgba = colors.CONFIRMED_BLUE

                        actor.update_pos(target_tile.grid_x, target_tile.grid_y)
                        actor.has_moved = True
                    
                    self.clean_selecteds()

                elif self.selected_action == "command":
                    if not target_tile.actor:
                        print("No target selected!")
                    elif self.selected_tile.actor.has_acted:
                        print("Actor has already acted!")
                    else:
                        command = self.selected_command
                        target = target_tile.actor
                        command.target = target
                        actor.has_acted = True

                        self.selected_tile.rgba = colors.CONFIRMED_BLUE
                        self.game.event_list.append(command)

                    self.clean_selecteds()
                
    def pass_turn(self):
        print("turn passes!")
        game = self.game
        for event in game.event_list:
            if type(event) is dict:
                msg = event
            else:
                msg = event.execute()

            if msg:
                print(f"{msg.get('msg', f'no msg to show... {event}')}")
            else:
                print(f"{event}")

        game.event_list = []
        for actor in game.actors:
            actor.clean_turn_state()

        for row in self.grid:
            for tile in row:
                tile.rgba = colors.BASIC_BLACK

        # import pdb; pdb.set_trace()


class GameApp(App):
    pass

if __name__ == '__main__':
    GameApp().run()
