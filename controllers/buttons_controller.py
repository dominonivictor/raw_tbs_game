from kivy.factory import Factory
from kivy.app import App
import misc.game_states as gs

from components.jobs_commands import gen_jobs_list
from components.equips_commands import gen_equips_list
from controllers.board_controller import (highlight_attackable_spaces,
clean_tiles, clean_hl_tiles)

def minor_btn_on_press(minor_btn):
    '''
    TAGS: BOARD, COMMAND?
    '''
    #needs to know too much of the board...? kinda yeah... also about the framework...
    app = App.get_running_app()
    board = app.root.ids.puzzle
    board.set_selected_action("command")
    command = minor_btn.command
    board.selected_command = command
    start_tile = board.selected_tile

    clean_hl_tiles(board, color='original_color')
    highlight_attackable_spaces(command, start_tile)
    board.state = gs.TARGETING


def minor_box_update_list(box, new_list):
    '''
    TAGS: BTN BOX, COMMAND?
    '''
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
    '''
    TAGS: BOARD, LOG_TEXT
    '''
    app = App.get_running_app()
    log_text = app.root.ids.log_text
    board = app.root.ids.puzzle

    if board.selected_tile and board.selected_tile.actor:
        board.state = gs.TARGETING
        board.selected_action = "move"
        log_text.text += "targeting mode\n"
    else:
        log_text.text += "No actor selected\n"

def major_btn_update_minor_box(new_list):
    '''
    TAGS: MINOR BOX, BOARD, LOG_TEXT
    '''
    app = App.get_running_app()
    board = app.root.ids.puzzle
    minor_box = app.root.ids.minor_options

    #needs to be commands    
    board.state = gs.TARGETING
    board.selected_action = "command"
    minor_box.update_commands_list(new_list) #jobs_list comes from import

def gen_major_box_widgets(box):
    '''
    TAGS: MAJOR BOX
    '''
    from main import MajorOptionsButton
    #too hard coded! but okish
    text_list = ["move", "learn_job", "equip_equip"]
    box.btns_list = (MajorOptionsButton(text=t) for t in text_list)

    for btn in box.btns_list:
        box.add_widget(btn)

def handle_major_options_btns(box):
    '''
    TAGS: MAJOR BOX
    '''
    if box.text == 'move':
        major_move_btn()
    elif box.text == 'learn_job':
        jobs_list = gen_jobs_list()
        major_btn_update_minor_box(jobs_list)
    elif box.text == 'equip_equip':
        equips_list = gen_equips_list()
        major_btn_update_minor_box(equips_list)
    else:
        print(f"another button with no on_press func yet")
