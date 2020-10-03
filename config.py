from player import Player


class Config:
    def __init__(self, **kwargs):
        self.p1 = kwargs.get('p1', Player(name='P1', initial_actors="fpt"))
        self.p2 = kwargs.get('p2', Player(name='P2', initial_actors="oca"))
        #self.ini_spaces = kwargs.get("ini_spaces",
        #        [])


    def set_player_actor(self, player_slug, actor):
        eval(f'self.{player_slug}.add_actor(actor)')

    def set_player_equip(self, player_slug, equip):
        eval(f'self.{player_slug}.add_equip(item)')

    def set_player_job(self, player_slug, job):
        eval(f'self.{player_slug}.add_job(job)')

    def remove_player_actor(self, player_slug, actor, index=-1):
        eval(f'self.{player_slug}.remove_actor(actor, index)')

    def remove_player_equip(self, player_slug, equip, index=-1):
        eval(f'self.{player_slug}.remove_equip(item, index)')

    def remove_player_job(self, player_slug, job, index=-1):
        eval(f'self.{player_slug}.remove_job(job, index)')
