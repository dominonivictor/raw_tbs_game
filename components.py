from statuses import StatusList

class Actor():
    def __init__(self, name, hp, def_stat, atk_stat, skills=[]):
        self.name = name
        self.hp = hp
        self.max_hp = Stat(value=hp.value)
        self.def_stat = def_stat 
        self.atk_stat = atk_stat
        self.statuses = StatusList()
        self.statuses.owner = self
        self.skills = SkillsList()
        self.skills.owner = self
        for skill in skills:
            self.skills.add_skill(skill)
    
class Stat():
    def __init__(self, value):
        self.value = value

