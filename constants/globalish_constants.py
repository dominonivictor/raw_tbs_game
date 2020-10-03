#TEST CONFIG adding stuff as arg  when calling main.py and setting up for
#success and optional settings and stuff! creating custom stuff, wow...
#programming is so great, need to go steadly and surely, focus one step at a time
GRID_SIZE = 3
I_ACTORS_NUM = 6
T_COORDS_RANDOM = {}
T_COORDS_BLANK = {"mountain": [], "forest": []}
#3x3 MAPS! could be larger... but are intended for 3x3
#maybe this stuff should have initial actors values in them too...
TEST_MAP_FOREST = {"mountain": [], "forest": [(x, 1) for x in range(3)]}
TEST_MAP_MOUNTAIN = {"mountain": [(1, y) for y in range(3)], "forest": []}
TEST_MAP_MOVE_SPACES_1 = {"mountain": [(1, 2)], "forest": [(0, 1), (2, 1)]}
I_SPACES_TEST_1 = [(1, 1)]
I_SPACES_TEST_2 = [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2)]

#"normal" config
GRID_SIZE_BASE = 13
# 13x13 board
I_SPACES_BASE = [(4, 4), (6, 4), (8, 4), (4, 8), (6, 8), (8, 8)]
