from components.statuses import DefUp, SpdUp, AtkUp, MaxHpUp, IncomeUp
from components.commands import Command, Attack
import constants.commands_cons as comm_cons

class Job():
    def __init__(self, **kwargs):
        self.owner = kwargs.get('owner', None)
        self.name = kwargs.get('name', "Jobless")
        self.category = kwargs.get('category', "good for nothing")
        self.commands = kwargs.get('commands', []) #which should be unique for each 
        self.passives = kwargs.get('passives', []) #which are basically perma statuses!


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
            for status in self.passives:
                self.owner.statuses.remove_status(status)

            self.owner = None 


#TODO: next place i shall clean up

class Guardian(Job):
    def __init__(self, owner=None, name="Guardian", category="Tank?, True Tank", commands=[Command(**comm_cons.PERFECT_COUNTER)], passives=[DefUp(timer=-1)]):
        super().__init__(owner=owner, name=name, category=category, commands=commands, passives=passives)

class Thief(Job):
    def __init__(self, owner=None, name="Thief", category="DPS/Utility", commands=[Attack(**comm_cons.TOXIC_SHOT)], passives=[SpdUp(timer=-1)]):
        super().__init__(owner=owner, name=name, category=category, commands=commands, passives=passives)

class Hunter(Job):
    def __init__(self, owner=None, name="Hunter", category="DPS/Tank", commands=[Attack(**comm_cons.TOXIC_SHOT)], passives=[AtkUp(timer=-1)]):
        super().__init__(owner=owner, name=name, category=category, commands=commands, passives=passives)

class Cook(Job):
    def __init__(self, owner=None, name="Cook", category="Utility/Tank", commands=[Attack(**comm_cons.TOXIC_SHOT)], passives=[MaxHpUp(timer=-1)]):
        super().__init__(owner=owner, name=name, category=category, commands=commands, passives=passives)

class Merchant(Job):
    def __init__(self, owner=None, name="Merchant", category="Utility/DPS", commands=[Attack(**comm_cons.TOXIC_SHOT)], passives=[IncomeUp(timer=-1)]):
        super().__init__(owner=owner, name=name, category=category, commands=commands, passives=passives)
