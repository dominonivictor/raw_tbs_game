from components.stats import Stats
from components.coordinate import Coordinate


class CombatComponent():
    def __init__(self, **kwargs):
        self.movable = kwargs.get("movable", False)
        self.pushable = kwargs.get("pushable", False)

        self.blocks = kwargs.get("blocks")
        self.is_physical = kwargs.get("is_physical", True)

        self.size = kwargs.get("size")
        self.owner = kwargs.get("owner")

        self.stats = kwargs.get("stats")
        self.stats = Stats(stats=stats)

        status_list = kwargs.get("status_list", [])
        self.passives = PassivesManager(status_list=status_list)

        coordinate = kwargs.get("coordinate")
        self.coords = Coordinate(coordinate=coordinate)
        