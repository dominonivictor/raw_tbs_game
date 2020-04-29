import constants.equips_cons as con


class Equip():
    def __init__(self, **kwargs):
        self.id = kwargs.get("id")
        self.name = kwargs.get("name", "Lostvayne")
        self.value = kwargs.get("value", 10)
        self.statuses = kwargs.get("statuses", [])
        self.category = kwargs.get("category", "Forgotten")
        self.element = kwargs.get("element", None)
        self.owner = kwargs.get("owner", None)

        from components.commands import get_new_command_by_id
        commands = kwargs.get("commands_func_params")
        self.commands = [get_new_command_by_id(id=commands)]

    def equip(self, owner):
        new_commands_list = []
        self.owner = owner

        from components.commands import get_new_command_by_id
        for command in self.commands:
            new_command = get_new_command_by_id(**command.__dict__)
            new_command.owner = self.owner
            new_commands_list.append(new_command)
            self.owner.commands.add_command(new_command, category="equip")

        self.commands = new_commands_list

        from components.statuses import get_new_status_by_id
        for status in self.statuses:
            new_status = get_new_status_by_id(**status.__dict__)
            new_status.owner = self.owner
            # status.target = self.owner
            self.owner.statuses.add_status(status)

        self.owner.equip = self

    def unequip(self):
        if self.owner:
            for command in self.commands:
                self.owner.commands.remove_command(command, category="equip")
            for status in self.statuses:
                self.owner.statuses.remove_status(status)

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
        string = f"""{self.name}, value: {self.value}, element: {self.element.name if self.element else "none"}
            equip_statuses: {[s.name for s in self.statuses]}, equip_commands: {[c.name for c in self.commands]}
        """
        return string

def get_new_equip_by_id(**kwargs):
    equips = {
        "zarabatana": Equip(**{**con.ZARABA, **kwargs}),
        "dagger": Equip(**{**con.DAGGER, **kwargs}),
        "cauldron": Equip(**{**con.CAULDRON, **kwargs}),
        "shield": Equip(**{**con.SHIELD, **kwargs}),
    }
    return equips.get(kwargs.get("id"))
