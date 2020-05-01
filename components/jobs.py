from components.statuses import get_new_statuses_by_ids
from components.commands import Command, Attack, CopyCat, Mixn
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
        # 
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
                self.owner.commands.add_command(command, category="job")
    
    def learn(self, owner):
        if owner.job:
            owner.job.unlearn()
        job.owner = owner
        owner.job = job
        owner.job.initialize()


    def unlearn(self):
        for command in self.commands:
            self.owner.commands.remove_command(command, category="job")
        for status in self.passives:
            self.owner.statuses.remove_status(status)

        self.owner = None 

    def pass_turn(self):
        pass


#TODO: next place i shall clean up

class Guardian(Job):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

class Thief(Job):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

class Hunter(Job):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

class Cook(Job):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

class Merchant(Job):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
