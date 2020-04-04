

class SkillList():
    def __init__(self):
        self.list = []

    def add_skill(self, skill):
        skill.owner = self
        self.list.append(skill)

    def _remove_skill(self, skill): 
        skill.remove_skill()   
        self.list.remove(skill)


class Skill():
    #skill is a command
    def __init__(self, name, target, owner, category='Queen Mother Skill'):
        self.name = name
        self.target = target
        self.owner = owner
        self.category = category
        self.description = 
