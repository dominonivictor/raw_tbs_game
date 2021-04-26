from components.statuses import StatusManager
from components.stats import Stats
from components.command_list import CommandsManager
from components.combat import CombatComponent
from game_eye import GameEye


class Actor():
    def __init__(self, **kwargs):
        self.name = kwargs.get("name", "Nameless")
        self.letter = kwargs.get("letter", "X")
        self.kingdom = kwargs.get("kingdom", "reptalia")
        self.animal = kwargs.get("animal", "fox")

        self.combat = CombatComponent(**kwargs)

        # self.stats = Stats(stats=kwargs.get("stats")) 
        # self.statuses = StatusManager() #same thing as passives manager, worth merging i think
        # self.statuses.owner = self
        # commands_ids = kwargs.get("commands_ids", [])
        # self.commands = CommandsManager(owner=self, commands_ids=commands_ids)

        self.job = kwargs.get("job", None)
        if self.job:
            self.learn_job(job)

        self.equip = kwargs.get("equip", None)
        if self.equip:
            self.add_equip(self.equip)

        # self.x = kwargs.get("x", 0)
        # self.y = kwargs.get("y", 0)
        self.has_moved = False
        self.has_acted = False

        self.game_eye = GameEye.instance()

    @property
    def stats(self):
        return self.combat.stats

    @property
    def statuses(self):
        return self.combat.statuses

    @property
    def commands(self):
        return self.combat.commands

    @property
    def x(self):
        return self.combat.coords.x

    @property
    def y(self):
        return self.combat.coords.y
     

    # I think these could be called directly... no need for extra layers...
    def show_statuses(self):
        return self.statuses.show_statuses()

    def show_commands(self):
        return self.commands.show_commands()
        
    # maybe do the same with these? do we really need owner self and stuff...
    def learn_job(self, job):
        job.learn(owner=self)
        
    def add_equip(self, item):
        item.equip(owner=self)

    def unequip(self):
        self.equip.unequip()

    def show_battle_stats(self):
        string = f"""
        Name: {self.name}
        Animal: {self.animal}
        Kingdom: {self.kingdom}
        HP: {self.stats.hp}/{self.stats.max_hp}
        ATK: {self.stats.at}
        DEF: {self.stats.df}
        SPD: {self.stats.sp}
        Statuses: {self.show_statuses()}
        Commands: {self.show_commands()}
        x, y: {self.x}, {self.y}
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
        if self.equip: self.equip.pass_time()
        if self.job: self.job.pass_time()

    def take_damage(self, value):
        # where is the thing calculated? def and atk bonus and stuff? in Command?
        hp = self.stats.hp
        # would a survive with one 1 hp/tryndamere ult kind of passive be here? 
        # maybe it could, but it would be better if a combat handler did it.
        # something like: self.combat.calculate_take_damage(value)
        self.stats.hp = hp - value if hp - value >= 0 else 0

    def heal_damage(self, value):
        hp = self.stats.hp
        stats_max_hp = self.stats.max_hp
        final_value = value + hp if hp + value <= stats_max_hp else stats_max_hp 
        # same thing from function above here!
        self.stats.hp = final_value

    def list_commands(self):
        return self.commands.list

    def has_command(self, command_id):
        for comm in self.commands.list:
            if comm.id == command_id:
                return True
        
        return False

    def get_command_by_id(self, id_):
        return self.commands.get_command_by_id(id_)

    # TODO: think better about these statuses functions... 
    # they really should be in the manager... or have a better API
    def list_statuses(self):
        return self.statuses.list

    def has_status(self, status_id):
        for status in self.statuses.list:
            if status.id == status_id:
                return True

        return False
    
    def get_status(self, status_id):
        for status in self.statuses.list:
            if status.id == status_id:
                return status
        return None

    def set_pos(self, x, y):
        self.x = x
        self.y = y
