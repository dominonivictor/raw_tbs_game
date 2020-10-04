from constants import colors

class UIMoveCommand():
    def __init__(self, **kwargs):
        self.current_tile = kwargs.get("current_tile")
        self.target_tile = kwargs.get("target_tile")
        self.board = kwargs.get("board")
        self.actor = kwargs.get("actor")

    def execute(self):
        current_coord = (self.current_tile.grid_x, self.current_tile.grid_y)
        target_coord = (self.target_tile.grid_x, self.target_tile.grid_y)
        actor = self.board.game.pop_actor_at_coord(current_coord)
        self.board.game.add_actor_at_coord(actor, target_coord)
        # UI board stuff
        self.target_tile.actor = actor
        self.current_tile.actor = None
        x, y = target_coord
        self.current_tile.rgba = self.board.game.grid[x][y].color
        self.current_tile.text = ""
        self.target_tile.text = self.target_tile.actor.letter
        # EXPERIMENTAL:
        self.target_tile.color = self.target_tile.actor.owner.color
        self.target_tile.set_color(colors.WALKABLE_BLUE)

        self.board.selected_tile = self.target_tile

        # actor stuff
        actor.update_pos(self.target_tile.grid_x, self.target_tile.grid_y)
        actor.has_moved = True

