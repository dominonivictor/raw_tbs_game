from components.commands import Command
import constants.job_commands_cons as cons

class LearnJobCommand(Command):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.job = kwargs.get("job")

    def execute(self):
        self.target.learn_job(self.job)
        return {"msg": self.target.name + self.description}

def gen_jobs_list():
    return [
        LearnJobCommand(**cons.GUARDIAN),
        LearnJobCommand(**cons.THIEF),
        LearnJobCommand(**cons.MERCHANT),
        LearnJobCommand(**cons.HUNTER),
        LearnJobCommand(**cons.COOK),
    ]
