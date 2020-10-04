from constants.colors import PLAYER_BLUE

class Player():
    def __init__(self, name="No named Player", **kwargs):
        self.name = name
        self.actors = []
        self.equips = [None, None, None]
        self.jobs = [None, None, None]
        self.initial_actors = kwargs.get("initial_actors", "fff")
        self.color = kwargs.get("color", PLAYER_BLUE)

    def replace_initial_actor_at_i(self, index, new_actor):
        actors = list(self.initial_actors)
        actors[index] = new_actor
        self.initial_actors = ''.join(actors)

    def update_initial_actors(self, actors_str):
        self.initial_actors = actors_str

    def add_actor(self, actor):
        self.actors.append(actor)
        actor.owner = self

    def add_job(self, job):
        self.jobs.append(job)
        job.owner = self

    def add_equip(self, equip):
        self.equips.append(equip)
        equip.owner = self

    def remove_last_actor(self, index=-1):
        last_actor = self.actors.pop(index)
        last_actor.owner = None

    def remove_last_equip(self, index=-1):
        last_equip = self.equips.pop(index)
        last_equip.owner = None

    def remove_last_job(self, index=-1):
        last_job = self.jobs.pop(index)
        last_job.owner = None

    def show_stuff(self, index):
        return f"Actor: {self.initial_actors[index]}"
#        return (
#            f"Actor: {self.actors[index].name if self.actors[index] else 'no actor'}"
#            f"Jobs: {self.jobs[index].name if self.jobs[index] else 'no job'}"
#            f"Equips: {self.equips[index].name if self.equips[index] else 'no equip'}"
#        )

    def __repr__(self):
        return (f"{{ 'name': {self.name}, 'actors': {self.actors}, 'initial_actors':"
                f"{self.initial_actors}  }}")
