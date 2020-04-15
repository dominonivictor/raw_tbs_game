from components.commands import Command
import constants.job_commands_cons as cons

class LearnJobCommand(Command):
    def __init__(self, target=None, name="go get a job", 
    description="Getchoself a job", category="learn_job", job=None):
        super().__init__(target=target,  name=name, description=description, category=category)
        self.job = job

    def execute(self):
        self.target.learn_job(self.job)
        return {"msg": self.target.name + self.description}

class GuardianCommand(LearnJobCommand):
    def __init__(self, owner=None, target=None, name=cons.GUARDIAN["name"], 
    description=cons.GUARDIAN["description"], category=cons.GUARDIAN["category"], job=cons.GUARDIAN["job"]):
        super().__init__(target=target, name=name, description=description, 
        category=category, job=job)

    def execute(self):
        super().execute()

class ThiefCommand(LearnJobCommand):
    def __init__(self, owner=None, target=None, name=cons.THIEF["name"], 
    description=cons.THIEF["description"], category=cons.THIEF["category"], job=cons.THIEF["job"]):
        super().__init__(target=target, name=name, description=description, 
        category=category, job=job)

    def execute(self):
        super().execute()

class MerchantCommand(LearnJobCommand):
    def __init__(self, owner=None, target=None, name=cons.MERCHANT["name"], 
    description=cons.MERCHANT["description"], category=cons.MERCHANT["category"], job=cons.MERCHANT["job"]):
        super().__init__(target=target, name=name, description=description, 
        category=category, job=job)

    def execute(self):
        super().execute()

class HunterCommand(LearnJobCommand):
    def __init__(self, owner=None, target=None, name=cons.HUNTER["name"], 
    description=cons.HUNTER["description"], category=cons.HUNTER["category"], job=cons.HUNTER["job"]):
        super().__init__(target=target, name=name, description=description, 
        category=category, job=job)

    def execute(self):
        super().execute()

class CookCommand(LearnJobCommand):
    def __init__(self, owner=None, target=None, name=cons.COOK["name"], 
    description=cons.COOK["description"], category=cons.COOK["category"], job=cons.COOK["job"]):
        super().__init__(target=target, name=name, description=description, 
        category=category, job=job)

    def execute(self):
        super().execute()


jobs_list = [
    GuardianCommand(),
    ThiefCommand(),
    MerchantCommand(),
    HunterCommand(),
    CookCommand(),
]