from game import Game
from functions.grid_patterns import region


def test_initial_game_setup():
    # 3 actors
    initial_v = {"actors_num": 2, "jobs_num": 0, "equips_num": 0}
    ini_spaces = [(0, 0), (0, 1), (0, 2), (2, 2)]
    GRID_SIZE = 3
    game = Game(grid_size=GRID_SIZE, initial_values=initial_v, ini_spaces=ini_spaces)
    game.initial_setup()
    count_actors = 0
    for x, y in region(GRID_SIZE - 1, GRID_SIZE - 1):
        if game.has_actor_on_xy(x, y):
            count_actors += 1

    assert count_actors == 4
