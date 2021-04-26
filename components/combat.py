from components.stats import Stats
from components.coordinate import Coordinate
from constants.misc import sizes

class CombatComponent():
    def __init__(self, **kwargs):
        # Representation
        # ? don't think should be here...

        # Regarding spatial restrictions
        self.movable = kwargs.get("movable", False)
        self.blocks_move = kwargs.get("blocks_move")
        self.blocks_sight = kwargs.get("blocks_sight")
        # self.swimmable = kwargs.get("swimmable")
        # self.z? height

        self.size = kwargs.get("size", sizes.SMALL)
        self.mass = kwargs.get("mass")

        # self.is_physical = kwargs.get("is_physical", True)
        self.owner = kwargs.get("owner")

        self.stats = kwargs.get("stats")
        self.stats = Stats(stats=self.stats)

        commands_list = kwargs.get("commands_list", [])
        self.commands = CommandsManager(commands_list=commands_list)

        status_list = kwargs.get("status_list", [])
        # TODO: these are basically the same, should be merged! 
        self.passives = PassivesManager(status_list=status_list)
        self.statuses = StatusesManager(status_list=status_list)

        coords = kwargs.get("coords")
        self.coords = Coordinate(coords=coords)
        
'''
{
    "movable": False,
    "blocks_move": False,
    "blocks_sight": False,
    "size": 0,
    "mass": 0,
    "owner": None,
    "stats": None,
    "commands_list": [],
    "passives_list": [],
    "coords": (0, 0),
}
'''