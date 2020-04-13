import constants.weapons_constants as con

class Weapon():
    def __init__(self, name="Lostvayne", value=10, statuses=[], commands=[], category="Forgotten", owner=None, element=None):
         self.name = name
         self.value = value
         self.statuses = statuses
         self.commands = commands
         self.category = category
         self.element = element
         self.owner = owner

    def equip(self, owner):
        self.owner = owner
        for command in self.commands:
            self.owner.commands.add_command(command)
        for status in self.statuses:
            self.owner.statuses.add_status(status)

    def unequip(self):
        for command in self.commands:
            self.owner.commands.remove_command(command)
        for status in self.statuses:
            self.owner.statuses.remove_status(status)

        self.owner = None

    def add_element(self, element):
        #go into added command and apply the status thingy
        element.owner = self
        for command in self.commands:
            command.status_dict.update(element.status_dict)

        if self.owner:
            for command in self.owner.commands.list:
                for w_command in self.commands:
                    if w_command.name == command.name:
                        command.status_dict.update(element.status_dict)

        self.element = element

class Zarabatana(Weapon):
    def __init__(self, name=con.ZARABA["name"], value=con.ZARABA["value"], statuses=con.ZARABA["statuses"], 
    commands=con.ZARABA["commands"], category=con.ZARABA["category"]):
        super().__init__(name=name, value=value, statuses=statuses, commands=commands, 
        category=category)

class Dagger(Weapon):
    def __init__(self, name=con.DAGGER["name"], value=con.DAGGER["value"], statuses=con.DAGGER["statuses"], 
    commands=con.DAGGER["commands"], category=con.DAGGER["category"]):
        super().__init__(name=name, value=value, statuses=statuses, commands=commands, 
        category=category)

class Cauldron(Weapon):
    def __init__(self, name=con.CAULDRON["name"], value=con.CAULDRON["value"], statuses=con.CAULDRON["statuses"], 
    commands=con.CAULDRON["commands"], category=con.CAULDRON["category"]):
        super().__init__(name=name, value=value, statuses=statuses, commands=commands, 
        category=category)

class Shield(Weapon):
    def __init__(self, name=con.SHIELD["name"], value=con.SHIELD["value"], statuses=con.SHIELD["statuses"], 
    commands=con.SHIELD["commands"], category=con.SHIELD["category"]):
        super().__init__(name=name, value=value, statuses=statuses, commands=commands, 
        category=category)
