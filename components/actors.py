from components.statuses import StatusList
from components.commands import CommandList

class Actor():
    def __init__(self, name="Nameless", hp=666, def_stat=42, atk_stat=73, spd_stat=13, commands=[], job=None):
        self.name = name
        self.hp = hp
        self.max_hp = Stat(value=hp.value)
        self.def_stat = def_stat 
        self.atk_stat = atk_stat
        self.spd_stat = spd_stat
        self.statuses = StatusList()
        self.statuses.owner = self
        self.commands = CommandList()
        self.commands.owner = self
        for command in commands:
            self.commands.add_command(command)

        self.job = job
        if self.job:
            self.job.owner = self
            self.job.initialize()

    def show_statuses(self):
        statuses = ''
        for status in self.statuses.list:
            statuses += f'{status.name}, '

        statuses = statuses[:-2] + '.'
        return statuses

    def show_commands(self):
        commands_str = ''
        i = 1
        for command in self.commands.list:
            commands_str = commands_str + f'({i}) {command.name} - '
            i += 1

        commands_str = commands_str[:-2] + '.'
        return commands_str
    
class Stat():
    def __init__(self, value):
        self.value = value

