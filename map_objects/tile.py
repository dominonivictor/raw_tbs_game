from constants.colors import BASIC_BLACK

class Tile():
    def __init__(self, **kwargs):
        self.move_cost = kwargs.get('move_cost', 1)
        self.group = kwargs.get('group', "groupless")
        self.is_blocked = kwargs.get('is_blocked', False)
        self.terrain = kwargs.get('terrain', None)
        self.structure = kwargs.get('structure', None)
        self.color = kwargs.get('color', BASIC_BLACK)