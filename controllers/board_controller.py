from kivy.app import App
from kivy.factory import Factory
import misc.game_states as gs
import constants.colors as colors
from collections import deque
from functions.grid_patterns import region
from components.ui_commands import UIMoveCommand


#The truth is this whole file should maybe be a class and its functions...
#OK stuff ain't pretty, but it's a start! Probably will have to change a lot of
#stuff and adding tests is the most secure way to do it. LEARN KIVY TESTS ASAP!
#Turn the code readable, separate stuff into smaller functions

def board_clean_selected_things(board, but_not_selected_tile=False, target_tile=None):
    '''
    TAGS: BOARD
    '''
    #This has to know too many details from the board. Maybe call a method from
    #board
    if not but_not_selected_tile:
        board.selected_tile = None
        board.selected_tile = target_tile

    board.selected_action = None
    board.selected_command = None
    board.state = gs.NORMAL

def create_grid(board, size, t_coords={}, i_spaces=[], actors=[]):
    '''
    TAGS: BOARD, GAME
    '''
    board.grid = []
    board.clear_widgets()
    board.rows, board.cols = size, size
    if(t_coords):
        t_coords = t_coords
    else:
        t_coords = {}

    board.game.create_grid(grid_size=board.grid_size, t_coords=t_coords)

    create_ui_grid(board, size)

def create_ui_tile(x, y, color):
    PT = Factory.PuzzleTile
    tile = PT()
    tile.grid_x, tile.grid_y = x, y
    set_tile_colors(tile, color)
    tile.actor = None

    return tile

def set_tile_colors(tile, color):
    tile.set_color(color)
    tile.set_original_color(color)
    tile.set_last_color(color)

def create_ui_grid(board, size):
    #could this be a region? maybe not due to the list of lists thing
    for i in range(board.rows):
        grid_cols = []
        for j in range(board.cols):
            color = board.game.get_tile(x=j, y=i).color
            tile = create_ui_tile(x=j, y=i, color=color)
            board.add_widget(tile)
            grid_cols.append(tile)

        board.grid.append(grid_cols)

    board.grid = list(map(list, zip(*board.grid)))

    #adding actors initially
    add_actors_in_starting_positions(board=board)



def select_tile(board, target_tile):
    '''
    TAGS: BOARD
    '''
    app = App.get_running_app()

    if board.state == gs.NORMAL:
        clean_hl_tiles(board, color='original_color')
        select_tile_normal_state(app=app, board=board, target_tile=target_tile)

    elif board.state == gs.TARGETING:
        select_tile_targeting_state(board=board, target_tile=target_tile)


def select_tile_normal_state(app, board, target_tile):
    '''
    TAGS: BOARD, GAME, ACTOR
    '''
    clean_hl_tiles(board, color='original_color')
    game_grid = board.game.grid
    selected_tile = board.selected_tile
    if selected_tile:
        #reset color
        selected_tile.set_color(selected_tile.get_original_color())

    actor = target_tile.actor if target_tile.actor else None
    if actor and not actor.has_moved:
        clean_tiles(board.movable_hl_tiles, board)
        clean_tiles(board.hl_tiles, board)
        clean_tiles(board.temp_hl_tiles, board)
        clean_tiles(board.attackable_hl_tiles, board)
        highlight_movable_spaces(actor=actor, start_tile=target_tile)

    target_tile.set_color(colors.SELECTED_RED)
    board.selected_tile = target_tile
    #checking if tile has actor
    actor_command_list = actor.list_commands() if actor else ""

    app.root.ids.stats_panel.update_actor_stats(actor)
    app.root.ids.minor_options.update_commands_list(actor_command_list)

def select_tile_targeting_state(board, target_tile):
    '''
    TAGS: BOARD, ACTOR
    '''
    #This is a little better to read, but a bit messy...
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
        if board.selected_action == "move":
            tiles = board.movable_hl_tiles
            targeting_move(actor=actor, current_tile=current_tile, target_tile=target_tile, movable_tiles=tiles, board=board)

        elif board.selected_action == "command":
            tiles = board.attackable_hl_tiles
            targeting_command(board=board, actor=actor, target_tile=target_tile, commandable_tiles=tiles)

        board_clean_selected_things(board=board, but_not_selected_tile=True, target_tile=target_tile)
    clean_all_tiles(board, color='original_color')

def targeting_move(actor, current_tile, target_tile, movable_tiles, board):
    '''
    TAGS: BOARD, GAME, ACTOR
    '''
    #TOO MUCH LOGIC HERE, NEED TO MAKE FLOW EASIER TO READ
    app = App.get_running_app()
    log_text = app.root.ids.log_text
    if actor.has_moved:
        log_text.text += "Actor has already moved!\n"
    elif target_tile.actor:
        log_text.text += "This tile is already ocuppied!\n"
    elif((target_tile.grid_x, target_tile.grid_y) not in movable_tiles):
        log_text.text += "Destination out of range!\n"
    else:
        #add this to commands list
        command = UIMoveCommand(
            current_tile=current_tile,
            target_tile=target_tile,
            board=board,
            actor=actor
        )
        board.game.event_list.append(command)
        #x0, y0 = current_tile.grid_x, current_tile.grid_y
        #x1, y1 = target_tile.grid_x, target_tile.grid_y
        x0, y0 = current_tile.center_x, current_tile.center_y
        x1, y1 = target_tile.center_x, target_tile.center_y
        board.add_line(target_tile, *(x0, y0), *(x1, y1))

    clean_tiles(board.hl_tiles, board)
    clean_tiles(board.temp_hl_tiles, board)

def change_actor_coords_in_game_grid(game, from_coord, to_coord):
    '''
    TAGS: GAME, ACTOR
    '''
    actor = game.pop_actor_at_coord(from_coord)
    game.add_actor_at_coord(actor, to_coord)

def targeting_command(board, actor, target_tile, commandable_tiles):
    '''
    TAGS: BOARD, GAME, ACTOR
    '''
    app = App.get_running_app()
    log_text = app.root.ids.log_text
    command = board.selected_command
    #ok this is not scalable at all..
    if not target_tile.actor and command.id not in ["multiply", "waterball"]:
        log_text.text += "No target selected!\n"
    elif board.selected_tile.actor.has_acted:
        log_text.text += "Actor has already acted!\n"
    elif((target_tile.grid_x, target_tile.grid_y) not in commandable_tiles):
        log_text.text += "Attack out of range!\n"
        clean_tiles(((x, y) for x, y in region(board.get_width(),
                                            board.get_height())), board,
                   color='last_color')
    else:
        target = target_tile.actor
        command.set_target(target)
        command.set_target_pos((target_tile.grid_x, target_tile.grid_y))
        actor.has_acted = True

        board.selected_tile.set_color(colors.WALKABLE_BLUE)
        board.game.event_list.append(command)

def pass_turn(board):
    '''
    TAGS: GAME, ACTOR
    '''
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

    board.remove_lines()


############## Temporary / Auxiliary functions

def add_actors_in_starting_positions(board):
    '''
    TAGS: BOARD, GAME, ACTOR
    '''
    #this is linked with game self.initial_setup()
    for i, (x, y) in enumerate(board.i_spaces):
        actor = board.game.actors[i]
        add_actor_at_xy(board, actor, x, y)

def add_actor_at_xy(board, actor, x, y):
    '''
    TAGS: GAME, ACTOR
    '''
    #this is doing way too much, need to centralize all this info...
    game = board.game
    tile = board.get_tile(x, y)
    game.add_actor_at_coord(actor, (x, y))
    tile.text = actor.letter
    tile.color = actor.owner.color
    tile.actor = actor
    actor.update_pos(x=x, y=y)

def highlight_movable_spaces(actor, start_tile):
    '''
    TAGS: GAME, ACTOR
    '''
    #TODO This needs to be generic to any amount of tiles and color
    app = App.get_running_app()

    n_moves = actor.get_spd()
    board = app.root.ids.puzzle
    game_grid = board.game.grid

    movable_spaces = calculate_dijkstras(start_tile, board, game_grid, calculate_cost_to_move, n_moves)

    highlight_tiles(tiles=movable_spaces, color=colors.WALKABLE_BLUE, board=board)

    board.set_movable_hl_tiles(movable_spaces)

def highlight_tiles(tiles, color, board):
    for x, y in tiles:
        board.get_tile(x, y).set_color(color)

def highlight_attackable_spaces(command, start_tile):
    '''
    TAGS: BOARD, GAME
    '''
    app = App.get_running_app()

    n_moves = command.max_range
    board = app.root.ids.puzzle
    game_grid = board.game.grid

    attackable_spaces = calculate_dijkstras(start_tile, board, game_grid, calculate_cost_to_attack, n_moves)

    for x, y in attackable_spaces:
        board.get_tile(x, y).set_color(colors.ATTACKABLE_RED)

    board.set_attackable_hl_tiles(attackable_spaces)


def calculate_dijkstras(start_tile, board, game_grid, step_cost_function, n_moves):
    '''
    TAGS: BOARD, GAME
    '''
    #calculate_cost_to_move -> for moving, calculate_cost_to_attack -> for attacking
    x, y = start_tile.grid_x, start_tile.grid_y
    closed_list = {}
    open_dict = {(x, y): {"dist": 0, "via": None}}
    tile_xy = True #just for getting in the loop
    while(tile_xy):
        tile_xy = min(open_dict, key=lambda k: open_dict[k]["dist"]) if open_dict else None
        if tile_xy:
            tile_dict = open_dict.pop(tile_xy)
            tile_neighbors = get_tile_neighbors(
                tile_xy=tile_xy, max_size=board.grid_size,
                game_grid=game_grid,
                closed_list=closed_list
            )

            for neigh_xy in tile_neighbors:
                neigh_dict = open_dict.get(neigh_xy, None)
                cost_for_step = step_cost_function(pos=neigh_xy, game_grid=game_grid)
                dist_now = tile_dict["dist"]
                final_dist = dist_now + cost_for_step
                if final_dist <= n_moves:
                    if(not neigh_dict or final_dist < neigh_dict["dist"]):
                        open_dict[neigh_xy] = {"dist": final_dist, "via": tile_xy}

            closed_list[tile_xy] = tile_dict

    return closed_list

def calculate_cost_to_move(pos, game_grid):
    #ALMOST good... but knows too much of how the game_grid works inside
    x, y = pos
    return game_grid[x][y].move_cost

def calculate_cost_to_attack(pos, game_grid):
    #very anti climatic, but may change in the future
    return 1

def get_tile_neighbors(tile_xy, max_size, game_grid, closed_list):
    #ALMOST good here too, knows too much of internals of game_grid
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

def clean_tiles(tiles, board, color=''):
    '''
    TAGS: BOARD, GAME
    '''
    #knows way too much of everything
    grid = board.game.grid
    for x, y in tiles:
        if is_xy_valid(x, y, board):
            tile = board.get_tile(x, y)
            if color == 'last_color':
                tile.set_color(tile.get_last_color())
            elif color == 'original_color':
                tile.set_color(tile.get_original_color())
            else:
                tile.set_color(grid[x][y].color)


def clean_all_tiles(board, color=''):
    clean_tiles(region(board.get_width(), board.get_height()), board,
                color=color)
    board.reset_hl_tiles()

def clean_hl_tiles(board, color=''):
    clean_tiles(board.temp_hl_tiles, board, color=color)
    clean_tiles(board.movable_hl_tiles, board, color=color)
    clean_tiles(board.attackable_hl_tiles, board, color=color)
    clean_tiles(board.hl_tiles, board, color=color)
    board.reset_hl_tiles()

def is_xy_valid(x, y, board):
    return 0 <= x < board.grid_size and 0 <= y < board.grid_size

def tile_on_hover(tile):
        app = App.get_running_app()
        board = app.puzzle
        #this scales badly as more categories come here... maybe all comms
        #should have their selected area
        if(board.selected_command and board.selected_command.category == "aoe"):
            c_x, c_y = tile.grid_x, tile.grid_y
            affected_tiles = set()
            for x, y in board.selected_command.tile_pattern:
                if is_xy_valid(c_x + x, c_y + y, board):
                    affected_tiles.add((c_x + x, c_y + y))

            high_tiles = set(board.temp_hl_tiles)
            clean_tiles(high_tiles, board,
                        color='last_color')
            for i, j in affected_tiles:
                    affected_tile = board.get_tile(i, j)
                    affected_tile.set_last_color(affected_tile.get_color())
                    affected_tile.set_color(colors.AOE_PURPLE)

            board.temp_hl_tiles  = affected_tiles
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
