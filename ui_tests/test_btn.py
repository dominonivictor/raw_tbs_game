import unittest

import os
import sys
import time
import os.path as op
from functools import partial
from kivy.clock import Clock

from main import GameApp
import constants.colors as colors
# when you have a test in <root>/tests/test.py
#main_path = op.dirname(op.dirname(op.abspath(__file__)))
#sys.path.append(main_path)


class Test(unittest.TestCase):
    def pause(*args):
        time.sleep(0.000001)

    '''
    everytime i make a new func i fall imeadiatly into old habits... maybe
    it`s ok... cause i can go back and refactor it, and train... but maybe
    is better to force myself to see it on the spot and do it only once
    def create_grid_test(self, app, *args):
        Clock.schedule_interval(self.pause, 0.000001)
        board = app.puzzle

        app.stop()

    don`t forget to add the func name inside a partial in test_btn()

    '''
    # main test function
    def create_grid_test(self, app, *args):
        Clock.schedule_interval(self.pause, 0.000001)

        board = app.puzzle
        create_grid_btn = app.create_grid_btn

        assert board.grid == []

        create_grid_btn.dispatch('on_release')
        assert board.grid != []

        app.stop()

    def red_highlight_tiles_test(self, app, *args):
        Clock.schedule_interval(self.pause, 0.000001)
        '''for this test i need a board, and an actor with skills, then i need
        to click on the actor and check the color of its surrounding tiles
        too bad it`s not checking the djakstras or anything... i could do
        a controlled board which output i know and check for it
        specifically...`'''
        board = app.puzzle
        create_grid_btn = app.create_grid_btn
        create_grid_btn.dispatch('on_release')

        actors = board.game.actors
        for actor in actors:
            print(f"{actor.name}, {actor.x}/{actor.y}")
            tile = board.get_tile(actor.x, actor.y)

        tile.dispatch('on_release')

        assert list(tile.rgba) == list(colors.SELECTED_RED)

        app.stop()

    def test_btn(self):
        app = GameApp()
        p = partial(self.create_grid_test, app)
        p = partial(self.red_highlight_tiles_test, app)
        Clock.schedule_once(p, 0.000001)
        app.run()

if __name__ == '__main__':
    unittest.main()
