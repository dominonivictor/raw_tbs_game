class Player():
    def __init__(self, name="No named Player"):
        self.name = name
        self.actors = []
        self.equips = []
        self.jobs = []
        self.spells = []

    def add_actor(self, actor):
        self.actors.append(actor)
        actor.owner = self

    def add_job(self, job):
        self.jobs.append(job)

    def add_equip(self, equip):
        self.equips.append(equip)

    def add_spell(self, spell):
        self.spells.append(spell)