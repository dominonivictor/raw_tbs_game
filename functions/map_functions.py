import constants.colors as colors
from random import randint

#TODO TOO MUCH REPETITION
def random_map_cost_tile_gen():
    r = randint(1, 12)
    if r in [1, 2]:
        move_cost = 2
        tile_color = colors.FOREST_GREEN
    elif r in [3, 4]:
        move_cost = 3
        tile_color = colors.MOUNTAIN_ORANGE
    else:
        move_cost = 1
        tile_color = colors.BASIC_BLACK

    return move_cost, tile_color

def defined_map_cost_tile_gen(x, y, t_coords):
    '''this is kinda messy and not so reusable...'''
    if (x, y) in t_coords["mountain"]:
        move_cost = 3
        tile_color = colors.MOUNTAIN_ORANGE
    elif (x, y) in t_coords["forest"]:
        move_cost = 2
        tile_color = colors.FOREST_GREEN
    else:
        move_cost = 1
        tile_color = colors.BASIC_BLACK

    return move_cost, tile_color
