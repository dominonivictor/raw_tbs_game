from player import Player


class Config:
    p1 = Player(name='P1')
    p2 = Player(name='P2')

    @classmethod
    def set_player_initial_actors(self, player_slug, actors_str):
        eval(f'self.{player_slug}.update_initial_actors({actors_str})')

    @classmethod
    def set_player_actor(self, player_slug, actor):
        eval(f'self.{player_slug}.add_actor(actor)')

    @classmethod
    def set_player_equip(self, player_slug, equip):
        eval(f'self.{player_slug}.add_equip(item)')

    @classmethod
    def set_player_job(self, player_slug, job):
        eval(f'self.{player_slug}.add_job(job)')

    @classmethod
    def remove_player_actor(self, player_slug, actor, index=-1):
        eval(f'self.{player_slug}.remove_actor(actor, index)')

    @classmethod
    def remove_player_equip(self, player_slug, equip, index=-1):
        eval(f'self.{player_slug}.remove_equip(item, index)')

    @classmethod
    def remove_player_job(self, player_slug, job, index=-1):
        eval(f'self.{player_slug}.remove_job(job, index)')

    @classmethod
    def print_self(self):
        return f"{{ 'config': {{ 'p1': {self.p1}, 'p2': {self.p2} }} }}"
