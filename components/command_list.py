class CommandList:
    def __init__(self, **kwargs):
        self.owner = kwargs.get("owner")
        self.base_list = []
        self.kingdom_list = []
        self.equip_list = []
        self.job_list = []
        self.list = []
        self.raw_commands_ids = kwargs.get("raw_commands_ids", [])
        self.init()

    def init(self):
        from components.commands import get_new_command_by_id

        commands = [
            get_new_command_by_id(id=comm_id) for comm_id in self.raw_commands_ids
        ]
        for command in commands:
            self.add_command(command, "base")
        self.add_kingdom_command()

    def add_command(self, command, category=""):
        for comm in self.list:
            if comm.id == command.id:
                print("Not able to add command cause it's already in the commands list")
        else:
            command.owner = self.owner
            self.list.append(command)
            if "base" in category:
                self.base_list.append(command)
            if "equip" in category:
                self.equip_list.append(command)
            if "job" in category:
                self.job_list.append(command)
            if "kingdom" in category:
                self.kingdom_list.append(command)

    def remove_command(self, command, category=""):
        command.owner = None
        self.list.remove(command)
        if "base" in category:
            self.base_list.remove(command)
        if "equip" in category:
            self.equip_list.remove(command)
        if "job" in category:
            self.job_list.remove(command)
        if "kingdom" in category:
            self.kingdom_list.remove(command)

    def add_eye(self):
        self.game_eye = self.owner.game_eye

    def add_kingdom_command(self):
        from components.commands import get_new_command_by_id

        # kinda ugly, stuff needs to come ready
        kingdom = self.owner.kingdom
        command = {
            "mamalia": get_new_command_by_id(id="multiply"),
            "reptalia": get_new_command_by_id(id="sun_charge"),
            "aves": get_new_command_by_id(id="golden_egg"),
        }.get(kingdom)
        self.add_command(command, category="kingdom")

    def show_commands(self):
        commands_str = ""
        i = 1
        for command in self.list:
            commands_str = commands_str + f"({i}) {command.name} - "
            i += 1

        commands_str = commands_str[:-2] + "."
        return commands_str

    def get_command_by_id(self, comm_id):
        for comm in self.list:
            if comm.id == comm_id:
                return comm

    def pass_time(self):
        pass
