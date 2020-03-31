class Attack():
    def __init__(self, owner, target, value):
        self.owner = owner
        self.target = target
        self.value = value

    def execute(self):
        final_value = self.owner.atk_stat.value + self.value - self.target.def_stat.value
        self.target.hp.value -= final_value
        return {"msg": f"{self.owner.name} attacks {self.target.name} for {final_value} damage"}

    def undo(self):
        #or maybe just do a heal command?
        v = self.value + self.owner.atk_stat.value - self.target.def_stat.value
        hp = self.target.hp.value
        max_hp = self.target.max_hp.value
        self.target.hp.value = v + hp if hp + v <= max_hp else max_hp 

class Heal():
    def __init__(self, owner, target, value):
        self.owner = owner
        self.target = target
        self.value = value

    def execute(self):
        #or maybe just do an attack command?
        v = self.value
        hp = self.target.hp.value
        max_hp = self.target.max_hp.value
        self.target.hp.value = v + hp if hp + v <= max_hp else max_hp 
        return {"msg": f"{self.owner.name} heals {v}, current hp: {self.target.hp.value}"}

    def undo(self):
        self.target.hp.value -= self.value
        return {"msg": f"{self.owner.name} attacks {self.target.name} for {self.value} damage"}

