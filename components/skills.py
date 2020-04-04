

class CommandList():
    def __init__(self):
        self.list = []

    def add_command(self, command):
        command.owner = self
        self.list.append(command)

    def _remove_command(self, command): 
        command.remove_command()   
        self.list.remove(command)


class Command():
    #Command is a command
    def __init__(self, name, target, owner, category='Queen Mother Command'):
        self.name = name
        self.target = target
        self.owner = owner
        self.category = category
        self.description = 
