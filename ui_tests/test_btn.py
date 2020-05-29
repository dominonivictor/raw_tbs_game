import unittest

import os
import sys
import time
import os.path as op
from functools import partial
from kivy.clock import Clock

from main import GameApp

# when you have a test in <root>/tests/test.py
#main_path = op.dirname(op.dirname(op.abspath(__file__)))
#sys.path.append(main_path)


class Test(unittest.TestCase):
    def pause(*args):
        time.sleep(0.000001)

    # main test function
    def create_grid_test(self, app, *args):
        Clock.schedule_interval(self.pause, 0.000001)

        board = app.puzzle
        create_grid_btn = app.create_grid_btn

        assert board.grid == []

        create_grid_btn.dispatch('on_release')
        assert board.grid != []

        # Comment out if you are editing the test, it'll leave the
        # Window opened.
        app.stop()

    def test_btn(self):
        app = GameApp()
        p = partial(self.create_grid_test, app)
        Clock.schedule_once(p, 0.000001)
        app.run()

if __name__ == '__main__':
    unittest.main()
