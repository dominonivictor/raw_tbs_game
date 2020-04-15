from kivy.app import App
from kivy.factory import Factory
import misc.game_states as gs
import constants.colors as colors



def grid_clean_selected_things(grid_obj, but_not_selected_tile=False, target_tile=None):
    if not but_not_selected_tile:
        grid_obj.selected_tile = None
        grid_obj.selected_tile = target_tile

    grid_obj.selected_action = None
    grid_obj.selected_command = None
    grid_obj.state = gs.NORMAL

def create_grid(grid_obj, size):
    grid_obj.grid = []
    grid_obj.clear_widgets()
    grid_obj.rows = size
    grid_obj.cols = size
    
    #making the grid
    PT = Factory.PuzzleTile
    for i in range(grid_obj.rows):
        grid_cols = []
        for j in range(grid_obj.cols):
            tile = PT(text=f'.')
            tile.actor = None
            tile.grid_x, tile.grid_y = j, i
            grid_obj.add_widget(tile)
            grid_cols.append(tile)

        grid_obj.grid.append(grid_cols)

    #adding actors initially
    add_actors_in_starting_positions(grid_obj=grid_obj)

def select_tile(grid, target_tile):
    app = App.get_running_app()
    if grid.state == gs.NORMAL:
        select_tile_normal_state(app=app, grid=grid, target_tile=target_tile)
    
    elif grid.state == gs.TARGETING:
        select_tile_targeting_state(grid=grid, target_tile=target_tile)


def select_tile_normal_state(app, grid, target_tile):
    if grid.selected_tile:
        grid.selected_tile.rgba = colors.BASIC_BLACK

    target_tile.rgba = colors.SELECTED_RED
    grid.selected_tile = target_tile
    actor = target_tile.actor if target_tile.actor else None
    actor_command_list = actor.commands.list if actor else []

    app.root.ids.stats_panel.update_actor_stats(actor)
    app.root.ids.minor_options.update_commands_list(actor_command_list)

def select_tile_targeting_state(grid, target_tile):

    if not grid.selected_tile:
        print("No tile selected!")
        grid.state = gs.NORMAL
    elif not grid.selected_tile.actor:
        print("no actor selected!")
        grid.state = gs.NORMAL
    else:
        current_tile = grid.selected_tile
        actor = current_tile.actor

        if grid.selected_action == "move":
            targeting_move(actor=actor, current_tile=current_tile, target_tile=target_tile)

        elif grid.selected_action == "command":
            targeting_command(grid=grid, actor=actor, target_tile=target_tile)

        grid_clean_selected_things(grid_obj=grid, but_not_selected_tile=True, target_tile=target_tile)

def targeting_move(actor, current_tile, target_tile):
    if actor.has_moved:
        print("actor has already moved!")
    elif target_tile.actor:
        print("This tile is already ocuppied!")
    else:
        target_tile.actor = actor
        current_tile.actor = None
        current_tile.rgba = colors.BASIC_BLACK
        current_tile.text = "."
        target_tile.text = target_tile.actor.name[0]
        target_tile.rgba = colors.CONFIRMED_BLUE

        actor.update_pos(target_tile.grid_x, target_tile.grid_y)
        actor.has_moved = True

def targeting_command(grid, actor, target_tile):
    if not target_tile.actor:
        print("No target selected!")
    elif grid.selected_tile.actor.has_acted:
        print("Actor has already acted!")
    else:
        command = grid.selected_command
        target = target_tile.actor
        command.target = target
        actor.has_acted = True

        grid.selected_tile.rgba = colors.CONFIRMED_BLUE
        grid.game.event_list.append(command)



def pass_turn(grid_obj):
    print("turn passes!")
    game = grid_obj.game
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

    for row in grid_obj.grid:
        for tile in row:
            tile.rgba = colors.BASIC_BLACK


############## Temporary / Auxiliary functions

def add_actors_in_starting_positions(grid_obj):
    for i, (x, y) in enumerate(grid_obj.initial_spaces):
        tile = grid_obj.grid[x][y]
        actor = grid_obj.game.actors[i]
        tile.text = actor.name[0]
        tile.actor = actor
        actor.update_pos(x=x, y=y)