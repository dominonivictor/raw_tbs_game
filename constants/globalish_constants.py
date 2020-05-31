#TEST CONFIG adding stuff as arg  when calling main.py and setting up for
#success and optional settings and stuff! creating custom stuff, wow...
#programming is so great, need to go steadly and surely, focus one step at a time
GRID_SIZE = 3
INITIAL_ACTORS_NUM = 6
INITIAL_SPACES = [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2)]

TEST_MAP_BLANK = {"mountain": [], "forest": []}
#3x3 MAPS! could be larger... but are intended for 3x3
#maybe this stuff should have initial actors values in them too...
TEST_MAP_FOREST = {"mountain": [], "forest": [(x, 1) for x in range(3)]}
TEST_MAP_MOUNTAIN = {"mountain": [(1, y) for y in range(3)], "forest": []}
TEST_MAP_MOVE_SPACES_1 = {"mountain": [(1, 2)], "forest": [(0, 1), (2, 1)]}
#for above player initial space should be (1, 1)

#"normal" config
#GRID_SIZE = 13
#INITIAL_SPACES = [(4, 4), (5, 4), (6, 4), (4, 8), (4, 6), (6, 8)]
