from components.statuses import StatusManager
from components.command_list import CommandList
from game_eye import GameEye


class Actor:
    def __init__(self, **kwargs):
        self.name = kwargs.get("name", "Nameless")
        self.letter = kwargs.get("letter", "X")
        self.kingdom = kwargs.get("kingdom", "reptalia")
        self.animal = kwargs.get("animal", "fox")
        self.hp_stat = kwargs.get("hp_stat", 10)
        self.max_hp_stat = kwargs.get("hp_stat", 10)
        self.atk_stat = kwargs.get("atk_stat", 2)
        self.def_stat = kwargs.get("def_stat", 0)
        self.spd_stat = kwargs.get("spd_stat", 4)
        self.income_stat = kwargs.get("income_stat", 2)

        self.statuses = StatusManager()
        self.statuses.owner = self

        raw_commands_ids = kwargs.get("commands_ids", [])
        self.commands = CommandList(owner=self, raw_commands_ids=raw_commands_ids)
        self.job = kwargs.get("job", None)
        if self.job:
            self.learn_job(job)

        self.equip = kwargs.get("equip", None)
        if self.equip:
            self.add_equip(self.equip)

        self.x = kwargs.get("x", 0)
        self.y = kwargs.get("y", 0)
        self.has_moved = False
        self.has_acted = False
        self.has_died = False
        self.game_eye = GameEye.instance()

    def show_statuses(self):
        return self.statuses.show_statuses()

    def show_commands(self):
        return self.commands.show_commands()

    def learn_job(self, job):
        job.learn(owner=self)
    
    def forget_job(self):
        self.job.forget()

    def add_equip(self, item):
        item.equip(owner=self)

    def unequip(self):
        self.equip.unequip()

    def show_battle_stats(self):
        string = f"""
        Name: {self.name}
        Animal: {self.animal}
        Kingdom: {self.kingdom}
        HP: {self.get_hp()}/{self.get_max_hp()}
        ATK: {self.get_atk()}
        DEF: {self.get_def()}
        SPD: {self.get_spd()}
        In: {self.get_inc()}
        Statuses: {self.show_statuses()}
        Commands: {self.show_commands()}
        x, y: {self.get_x()}, {self.get_y()}
        job: {self.job.get_name() if self.job else "Jobless"}
        equip: {self.equip.show_equip_stats() if self.equip else "No Equip"}
        """

        return string

    def update_pos(self, x, y):
        self.x = x
        self.y = y

    def clean_turn_state(self):
        self.has_acted = False
        self.has_moved = False

    def pass_time(self):
        self.commands.pass_time()
        self.statuses.pass_time()
        if self.equip:
            self.equip.pass_time()
        if self.job:
            self.job.pass_time()

    def take_damage(self, value):
        if not self.has_died:
            hp = self.get_hp()
            self.set_hp(hp - value if hp - value >= 0 else 0)
            if self.hp_stat == 0:
                self.has_died = True

    def heal_damage(self, value):
        if not self.has_died:
            hp = self.get_hp()
            max_hp = self.get_max_hp()
            final_value = value + hp if hp + value <= max_hp else max_hp
            self.set_hp(final_value)

    def list_commands(self):
        return self.commands.list

    def has_command(self, command_id):
        for comm in self.commands.list:
            if comm.id == command_id:
                return True
        return False

    def get_command_by_id(self, id_):
        return self.commands.get_command_by_id(id_)

    def list_statuses(self):
        return self.statuses.list

    def has_status(self, status_id):
        return self.statuses.has_status(status_id)

    def get_status(self, status_id):
        for status in self.statuses.list:
            if status.id == status_id:
                return status

        else:
            return None

    def get_hp(self):
        return self.hp_stat

    def set_hp(self, value):
        self.hp_stat = value

    def get_max_hp(self):
        return self.max_hp_stat

    def set_max_hp(self, value):
        self.max_hp_stat = value

    def get_atk(self):
        return self.atk_stat

    def set_atk(self, value):
        self.atk_stat = value

    def get_def(self):
        return self.def_stat

    def set_def(self, value):
        self.def_stat = value

    def get_spd(self):
        return self.spd_stat

    def set_spd(self, value):
        self.spd_stat = value

    def get_inc(self):
        return self.income_stat

    def set_inc(self, value):
        self.income_stat = value

    def set_pos(self, x, y):
        self.set_x(x)
        self.set_y(y)

    def set_x(self, x):
        self.x = x

    def set_y(self, y):
        self.y = y

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y
