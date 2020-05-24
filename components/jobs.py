from components.statuses import get_new_statuses_by_ids
import constants.commands_cons as comm_cons

class Job():
    def __init__(self, **kwargs):
        self.owner = kwargs.get('owner', None)
        self.name = kwargs.get('name', "Jobless")
        self.category = kwargs.get('category', "good for nothing")

        #separate this into a commands_list and status_list or similar
        #make it interact with the other apis a little more easily...
        #there is too much happening here!
        #this should come ready...

        commands_ids = kwargs.get('commands_ids', [])
        from components.commands import get_new_command_by_id
        commands = kwargs.get("commands", [])
        if not commands: 
            self.commands = [get_new_command_by_id(id=id_) for id_ in commands_ids] 
        else:
            self.commands = commands

        from components.statuses import get_new_statuses_by_ids
        passives_ids = kwargs.get('status_ids', [])
        passives_ids = [{"id": id_, "timer": -1} for id_ in passives_ids]
        self.passives = get_new_statuses_by_ids(status_list=passives_ids)


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
                passive.target = self.owner

    def apply_passives(self):
        if self.owner:
            self.owner.statuses.add_statuses_to_actor(statuses=self.passives)
            

    def apply_commands(self):
        if self.owner:
            for command in self.commands:
                self.owner.commands.add_command(command, category="job")
    
    def learn(self, owner):
        if owner.job:
            owner.job.unlearn()
        self.owner = owner
        owner.job = self
        self.initialize()


    def unlearn(self):
        for command in self.commands:
            self.owner.commands.remove_command(command, category="job")
        for status in self.passives:
            self.owner.statuses.remove_status(status)

        self.owner = None 

    def pass_time(self):
        pass

    def get_name(self):
        return self.name

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



