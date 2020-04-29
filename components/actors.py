from components.statuses import StatusList
from components.commands import CommandList
from game_eye import GameEye


class Actor():
    def __init__(self, **kwargs):
        self.name = kwargs.get("name", "Nameless")
        self.letter = kwargs.get("letter", "X")
        self.kingdom = kwargs.get("kingdom", "No kingdom")
        self.animal = kwargs.get("animal", "scrub")
        self.hp_stat = kwargs.get("hp_stat")
        self.max_hp_stat = Stat(value=kwargs.get("hp_stat").value)
        self.def_stat = kwargs.get("def_stat") 
        self.atk_stat = kwargs.get("atk_stat")
        self.spd_stat = kwargs.get("spd_stat")
        self.income_stat = kwargs.get("income_stat")
        self.statuses = StatusList()
        self.statuses.owner = self

        self.base_commands = kwargs.get("commands", [])
        self.commands = CommandList(owner=self)

        self.job = kwargs.get("job", None)
        if self.job:
            self.learn_job(job)

        self.equip = kwargs.get("equip", None)
        if self.equip:
            self.add_equip(equip)

        self.x = kwargs.get("x", 0)
        self.y = kwargs.get("y", 0)
        self.has_moved = False
        self.has_acted = False

        self.game_eye = GameEye.instance()

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

    def learn_job(self, job):
        if self.job:
            self.job.unlearn()
        job.owner = self
        self.job = job
        self.job.initialize()

    def add_equip(self, item):
        item.equip(owner=self)

    def unequip(self):
        self.equip.unequip()
        self.equip = None

    def show_battle_stats(self):
        string = f"""
        Name: {self.name}
        Animal: {self.animal}
        Kingdom: {self.kingdom}
        HP: {self.hp_stat.value}/{self.max_hp_stat.value}
        ATK: {self.atk_stat.value}
        DEF: {self.def_stat.value}
        SPD: {self.spd_stat.value}
        In: {self.income_stat.value}
        Statuses: {self.show_statuses()}
        Commands: {self.show_commands()}
        x, y: {self.x}, {self.y}
        job: {self.job.name if self.job else "Jobless"}
        equip: {self.equip.show_equip_stats() if self.equip else "No Equip"}
        """

        return string

    def update_pos(self, x, y):
        self.x = x
        self.y = y

    def clean_turn_state(self):
        self.has_acted = False
        self.has_moved = False

class Stat():
    def __init__(self, value):
        self.value = value

