from components.statuses import StatusList
from components.commands import CommandList

class Actor():
    def __init__(self, name, hp, def_stat, atk_stat, spd_stat, commands=[]):
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

    def show_statuses(self):
        statuses = ''
        for status in self.statuses.list:
            statuses += f'{status.name}, '

        statuses = statuses[:-2] + '.'
        return statuses

    def show_commands(self):
        commands = ''
        for command in self.commands.list:
            commands = commands + f'{command.name}, '

        commands = commands[:-2] + '.'
        return commands
    
class Stat():
    def __init__(self, value):
        self.value = value

