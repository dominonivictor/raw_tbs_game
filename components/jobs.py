from components.statuses import DefUp, SpdUp
from components.commands import SunCharge, ToxicShot

class Job():
    def __init__(self, owner=None, name="Jobless", category="good for nothing", commands=[], passives=[]):
        self.name = name
        self.category = category
        self.commands = commands
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


class Guardian(Job):
    def __init__(self, owner=None, name="Guardian", category="Tank", commands=[SunCharge()], passives=[DefUp(timer=-1)]):
        super().__init__(owner=owner, name=name, category=category, commands=commands, passives=passives)

class Thief(Job):
    def __init__(self, owner=None, name="Thief", category="DPS?", commands=[ToxicShot()], passives=[SpdUp(timer=-1)]):
        super().__init__(owner=owner, name=name, category=category, commands=commands, passives=passives)