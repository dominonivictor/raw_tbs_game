from kivy.factory import Factory
from kivy.app import App
from main import MajorOptionsButton
import misc.game_states as gs

from components.jobs_commands import jobs_list
from components.equips_commands import equips_list

def minor_btn_on_press(minor_btn):
    app = App.get_running_app()
    app.root.ids.puzzle.selected_action = "command"
    app.root.ids.puzzle.selected_command = minor_btn.command
    app.root.ids.puzzle.state = gs.TARGETING


def minor_box_update_list(box, new_list):
    box.clear_widgets()
    box.current_list = []
    if new_list:
        btn_factory = Factory.MinorOptionsButton
        for item in new_list:
            # Everything needs to be a command, learn job comm(ex), cause then the maintanance will be trivial
            new_btn = btn_factory(text=item.name)
            new_btn.command = item 
            box.add_widget(new_btn)
            box.current_list.append(item)


def major_move_btn():
    app = App.get_running_app()
    grid = app.root.ids.puzzle 

    if grid.selected_tile and grid.selected_tile.actor:
        grid.state = gs.TARGETING
        grid.selected_action = "move"
        print("targeting mode")
    else:
        print("No actor selected")

def major_btn_update_minor_box(new_list):
    app = App.get_running_app()
    grid = app.root.ids.puzzle 
    minor_box = app.root.ids.minor_options
    
    #needs to be commands    
    grid.state = gs.TARGETING
    grid.selected_action = "command"
    minor_box.update_commands_list(new_list) #jobs_list comes from import
    
def gen_major_box_widgets(box):
    box.btns_list = [
        MajorOptionsButton(text="move"),
        MajorOptionsButton(text="learn_job"),
        MajorOptionsButton(text="equip_equip"),
    ]

    for btn in box.btns_list:
        box.add_widget(btn)

def handle_major_options_btns(box):
    if box.text == 'move':
        major_move_btn()
    elif box.text == 'learn_job':
        major_btn_update_minor_box(jobs_list)
    elif box.text == 'equip_equip':
        major_btn_update_minor_box(equips_list)
    else:
        print(f"another button with no on_press func yet")