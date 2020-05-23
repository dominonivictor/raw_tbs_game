import constants.equips_cons as con
from components.statuses import PassivesList

class Equip():
    '''
        What i want this to do: handle an Equip object, with its commands, passives and elements
    '''
    def __init__(self, **kwargs):
        self.id = kwargs.get("id")
        self.name = kwargs.get("name", "Lostvayne")
        self.value = kwargs.get("value", 10)
        self.category = kwargs.get("category", "Forgotten")
        self.element = kwargs.get("element", None)
        self.owner = kwargs.get("owner", None)

        # this is getting very complex very quickly, the idea is to try making things
        # SRP standardized
        from components.statuses import get_new_statuses_by_ids
        status_list = kwargs.get("statuses", [])
        #all of statuses here will be passives, so the timer will be set to -1 (infinite until removed)
        self.passives = PassivesList()
        passives = get_new_statuses_by_ids(status_list=status_list) 
        for passive in passives:
            self.passives.add_passive(passive)

        commands = kwargs.get("commands_ids", [])
        self.commands = []
        for command in commands:
            self.add_command(command)

    def equip(self, owner):
        self.owner = owner
        for command in self.commands:
            command.owner = self.owner
            self.owner.commands.add_command(command, category="equip")

        for passive in self.passives.list:
            passive.owner = self.owner
            self.owner.statuses.add_status(passive)

        self.owner.equip = self

    def unequip(self):
        if self.owner:
            for command in self.commands:
                self.owner.commands.remove_command(command, category="equip")
            for status in self.statuses:
                self.owner.statuses.remove_status(status)

            self.owner.equip = None
            self.owner = None

    def add_element(self, element):
        #go into added command and apply the status thingy
        if self.element:
            self.remove_element(self.element)
        from components.elements import get_new_element_by_id
        new_element = get_new_element_by_id(id=element.id)
        new_element.owner = self
        for command in self.commands:
            command.statuses.add_status(new_element.statuses)

        self.element = new_element

    def remove_element(self, element):
        element.owner = None
        for command in self.commands:
            command.statuses.remove(element.status)

    def show_equip_stats(self):
        string = f"""
        {self.name}, 
        value: {self.value}, 
        element: {self.element.name if self.element else "none"}
        equip_statuses: {self.list_passives()}, 
        equip_commands: {[c.name for c in self.commands]}
        """
        return string

    def add_command(self, command_id):
        from components.commands import get_new_command_by_id
        for comm in self.commands:
            if comm.id == command_id:
                return
        else:
            new_comm = get_new_command_by_id(id=command_id)
            self.commands.append(new_comm)

    def pass_time(self):
        pass

    def list_passives(self):
        return self.passives.list

    def has_element(self):
        return bool(self.element)

def get_new_equip_by_id(**kwargs):
    equips = {
        "zarabatana": Equip(**{**con.ZARABA, **kwargs}),
        "dagger": Equip(**{**con.DAGGER, **kwargs}),
        "cauldron": Equip(**{**con.CAULDRON, **kwargs}),
        "shield": Equip(**{**con.SHIELD, **kwargs}),
    }
    return equips.get(kwargs.get("id"))
