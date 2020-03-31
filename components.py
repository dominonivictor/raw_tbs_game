class Actor():
    def __init__(self, name, hp, def_stat, atk_stat):
        self.name = name
        self.hp = hp
        self.max_hp = Stat(value=hp.value)
        self.def_stat = def_stat 
        self.atk_stat = atk_stat
    
class Stat():
    def __init__(self, value):
        self.value = value
