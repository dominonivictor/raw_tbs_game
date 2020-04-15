from components.statuses import DefUp, SpdUp, AtkUp, MaxHpUp, IncomeUp
from components.commands import SunCharge, ToxicShot

class Job():
    def __init__(self, owner=None, name="Jobless", category="good for nothing", commands=[], passives=[]):
        self.name = name
        self.category = category
        self.commands = commands #which should be unique for each 
        self.passives = passives #which are basically perma statuses!


    def initialize(self):
        self.apply_ownership()
        self.apply_passives()
        self.apply_commands()

    def apply_ownership(self):
        if self.owner:
            for command in self.commands:
                command.owner = self.owner
            for passive in self.passives:
                passive.owner = self.owner

    def apply_passives(self):
        if self.owner:
            for passive in self.passives:
                passive.target = self.owner
                self.owner.statuses.add_status(passive)
            

    def apply_commands(self):
        if self.owner:
            for command in self.commands:
                self.owner.commands.add_command(command)
    
    def unlearn(self):
        if self.owner:
            for command in self.commands:
                self.owner.commands.remove_command(command)
            for status in self.statuses:
                self.owner.statuses.remove_status(status)

            self.owner = None 


class Guardian(Job):
    def __init__(self, owner=None, name="Guardian", category="Tank", commands=[SunCharge()], passives=[DefUp(timer=-1)]):
        super().__init__(owner=owner, name=name, category=category, commands=commands, passives=passives)

class Thief(Job):
    def __init__(self, owner=None, name="Thief", category="DPS?", commands=[ToxicShot()], passives=[SpdUp(timer=-1)]):
        super().__init__(owner=owner, name=name, category=category, commands=commands, passives=passives)

class Hunter(Job):
    def __init__(self, owner=None, name="Hunter", category="DPS", commands=[ToxicShot()], passives=[AtkUp(timer=-1)]):
        super().__init__(owner=owner, name=name, category=category, commands=commands, passives=passives)

class Cook(Job):
    def __init__(self, owner=None, name="Cook", category="Utility", commands=[ToxicShot()], passives=[MaxHpUp(timer=-1)]):
        super().__init__(owner=owner, name=name, category=category, commands=commands, passives=passives)

class Merchant(Job):
    def __init__(self, owner=None, name="Merchant", category="Utility", commands=[ToxicShot()], passives=[IncomeUp(timer=-1)]):
        super().__init__(owner=owner, name=name, category=category, commands=commands, passives=passives)
