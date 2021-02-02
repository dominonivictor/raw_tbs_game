from player import Player
from constants.colors import PLAYER_RED, PLAYER_BLUE


class Config:
    p1 = Player(name="P1", color=PLAYER_RED)
    p2 = Player(name="P2", color=PLAYER_BLUE)

    @classmethod
    def clean_players(cls):
        cls.p1.reset_actors()
        cls.p2.reset_actors()