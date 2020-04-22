from kivy.app import App
from kivy.factory import Factory
import misc.game_states as gs
import constants.colors as colors
from collections import deque

def board_clean_selected_things(board, but_not_selected_tile=False, target_tile=None):
    if not but_not_selected_tile:
        board.selected_tile = None
        board.selected_tile = target_tile

    board.selected_action = None
    board.selected_command = None
    board.state = gs.NORMAL

def create_grid(board, size):
    board.grid = []
    board.clear_widgets()
    board.rows = size
    board.cols = size
    
    #making the grid
    PT = Factory.PuzzleTile
    for i in range(board.rows):
        grid_cols = []
        for j in range(board.cols):
            tile = PT(text=f'.')
            tile.actor = None
            tile.grid_x, tile.grid_y = j, i
            tile.rgba = board.game.grid[j][i].color
            board.add_widget(tile)
            grid_cols.append(tile)

        board.grid.append(grid_cols)

    board.grid = list(map(list, zip(*board.grid)))

    #adding actors initially
    add_actors_in_starting_positions(board=board)

def select_tile(board, target_tile):
    app = App.get_running_app()
    
    if board.state == gs.NORMAL:
        clean_tiles(board.highlighted_tiles, board)
        select_tile_normal_state(app=app, board=board, target_tile=target_tile)
    
    elif board.state == gs.TARGETING:
        select_tile_targeting_state(board=board, target_tile=target_tile)


def select_tile_normal_state(app, board, target_tile):
    game_grid = board.game.grid
    if board.selected_tile:
        x, y = board.selected_tile.grid_x, board.selected_tile.grid_y
        board.selected_tile.rgba = game_grid[x][y].color

    actor = target_tile.actor if target_tile.actor else None
    if actor and not actor.has_moved:
        clean_tiles(board.highlighted_tiles, board)
        highlight_movable_spaces(actor=actor, start_tile=target_tile)

    target_tile.rgba = colors.SELECTED_RED
    board.selected_tile = target_tile
    actor_command_list = actor.commands.list if actor else []

    app.root.ids.stats_panel.update_actor_stats(actor)
    app.root.ids.minor_options.update_commands_list(actor_command_list)

def select_tile_targeting_state(board, target_tile):
    app = App.get_running_app()
    log_text = app.root.ids.log_text
    if not board.selected_tile:
        log_text.text += "No tile selected!\n"
        board.state = gs.NORMAL
    elif not board.selected_tile.actor:
        log_text.text += "no actor selected!\n"
        board.state = gs.NORMAL
    else:
        current_tile = board.selected_tile
        actor = current_tile.actor
        high_tiles = board.highlighted_tiles
        if board.selected_action == "move":
            targeting_move(actor=actor, current_tile=current_tile, target_tile=target_tile, movable_tiles=high_tiles, board=board)

        elif board.selected_action == "command":
            targeting_command(board=board, actor=actor, target_tile=target_tile, commandable_tiles=high_tiles)

        board_clean_selected_things(board=board, but_not_selected_tile=True, target_tile=target_tile)
    clean_tiles(board.highlighted_tiles, board)

def targeting_move(actor, current_tile, target_tile, movable_tiles, board):
    app = App.get_running_app()
    log_text = app.root.ids.log_text
    if actor.has_moved:
        log_text.text += "Actor has already moved!\n"
    elif target_tile.actor:
        log_text.text += "This tile is already ocuppied!\n"
    elif((target_tile.grid_x, target_tile.grid_y) not in movable_tiles):
        log_text.text += "Destination out of range!\n"
    else:
        target_tile.actor = actor
        current_tile.actor = None
        x, y = target_tile.grid_x, target_tile.grid_y
        current_tile.rgba = board.game.grid[x][y].color
        current_tile.text = "."
        target_tile.text = target_tile.actor.letter
        target_tile.rgba = colors.WALKABLE_BLUE

        board.selected_tile = target_tile
        actor.update_pos(target_tile.grid_x, target_tile.grid_y)
        actor.has_moved = True

    clean_tiles(board.highlighted_tiles, board)

def targeting_command(board, actor, target_tile, commandable_tiles):
    app = App.get_running_app()
    log_text = app.root.ids.log_text
    if not target_tile.actor:
        log_text.text += "No target selected!\n"
    elif board.selected_tile.actor.has_acted:
        log_text.text += "Actor has already acted!\n"
    elif((target_tile.grid_x, target_tile.grid_y) not in commandable_tiles):
        log_text.text += "Destination out of range!\n"
    else:
        command = board.selected_command
        target = target_tile.actor
        
        command.target = target
        actor.has_acted = True

        board.selected_tile.rgba = colors.WALKABLE_BLUE
        board.game.event_list.append(command)

def pass_turn(board):
    app = App.get_running_app()
    log_text = app.root.ids.log_text
    log_text.text += "turn passes!\n"
    game = board.game
    for event in game.event_list:
        if type(event) is dict:
            msg = event
        else:
            msg = event.execute()

        if msg:
            log_text.text += f"{msg.get('msg', f'no msg to show... {event}')}\n"
        else:
            log_text.text += f"{event}\n"

    game.event_list = []
    for actor in game.actors:
        msg_list = actor.statuses.pass_time()
        actor.clean_turn_state()
        game.event_list.extend(msg_list)

    for row in board.grid:
        for tile in row:
            x, y = tile.grid_x, tile.grid_y
            tile.rgba = board.game.grid[x][y].color


############## Temporary / Auxiliary functions

def add_actors_in_starting_positions(board):
    for i, (x, y) in enumerate(board.initial_spaces):
        tile = board.grid[x][y]
        actor = board.game.actors[i]
        tile.text = actor.letter
        tile.actor = actor
        actor.update_pos(x=x, y=y)

def highlight_movable_spaces(actor, start_tile):
    app = App.get_running_app()

    n_moves = actor.spd_stat.value
    board = app.root.ids.puzzle
    ui_grid = board.grid
    game_grid = board.game.grid

    closed_list = calculate_dijkstras(start_tile, board, game_grid, calculate_cost_to_move, n_moves)
    
    for x, y in closed_list:
        ui_grid[x][y].rgba = colors.WALKABLE_BLUE

    board.highlighted_tiles = closed_list

def highlight_attackable_spaces(command, start_tile):
    app = App.get_running_app()

    n_moves = command.max_range
    board = app.root.ids.puzzle
    ui_grid = board.grid
    game_grid = board.game.grid

    closed_list = calculate_dijkstras(start_tile, board, game_grid, calculate_cost_to_attack, n_moves)
    
    for x, y in closed_list:
        ui_grid[x][y].rgba = colors.ATTACKABLE_RED

    board.highlighted_tiles = closed_list


def calculate_dijkstras(start_tile, board, game_grid, step_cost_function, n_moves):
    #calculate_cost_to_move -> for moving, calculate_cost_to_attack -> for attacking
    x, y = start_tile.grid_x, start_tile.grid_y
    closed_list = []
    open_dict = {(x, y): {"dist": 0, "via": None}}
    tile_xy = True #just for getting in the loop
    while(tile_xy):
        tile_xy = min(open_dict, key=lambda k: open_dict[k]["dist"]) if open_dict else None
        if tile_xy:
            tile_dict = open_dict.pop(tile_xy)
            tile_neighbors = get_tile_neighbors(tile_xy=tile_xy, max_size=board.grid_size, 
                                                game_grid=game_grid, closed_list=closed_list)

            for neigh_xy in tile_neighbors:
                neigh_dict = open_dict.get(neigh_xy, None)
                cost_for_step = step_cost_function(pos=neigh_xy, game_grid=game_grid)
                dist_now = tile_dict["dist"]
                final_dist = dist_now + cost_for_step
                if final_dist <= n_moves:
                    if(not neigh_dict or final_dist < neigh_dict["dist"]):
                        open_dict[neigh_xy] = {"dist": final_dist, "via": tile_xy}

            closed_list.append(tile_xy)

    return closed_list

def calculate_cost_to_move(pos, game_grid):
    x, y = pos
    return game_grid[x][y].move_cost

def calculate_cost_to_attack(pos, game_grid):
    return 1

def get_tile_neighbors(tile_xy, max_size, game_grid, closed_list):
    neighbors = []
    i, j = tile_xy
    if i - 1 >= 0:
        neighbors.append((i-1, j))
    if i + 1 <= max_size - 1:
        neighbors.append((i+1, j))
    if j - 1 >= 0:
        neighbors.append((i, j-1))
    if j + 1 <= max_size - 1:
        neighbors.append((i, j+1))

    for coords in neighbors:
        x, y = coords
        if(game_grid[x][y].is_blocked):
            neighbors.remove((x, y))

    return neighbors

def clean_tiles(tiles, board):
    grid = board.grid
    for x, y in tiles:
        grid[x][y].rgba = board.game.grid[x][y].color

    board.highlighted_tiles = []
    
'''
def create_graph(board, size):
    graph = {}
    for i in range(size):
        for j in range(size):
            graph[i, j] = []
            if i - 1 >= 0:
                graph[i, j].append((i-1, j))
            if i + 1 <= size - 1:
                graph[i, j].append((i+1, j))
            if j - 1 >= 0:
                graph[i, j].append((i, j-1))
            if j + 1 <= size - 1:
                graph[i, j].append((i, j+1))

    board.graph = graph
'''