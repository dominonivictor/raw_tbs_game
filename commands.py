import statuses as sts
import commands_constants as con

base_atk = 4
base_heal = 3

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
    def __init__(self, owner=None, target=None, value=0, name="Abyssal Lord Command", 
    description="Abyssal Lord Command Description", category="Abyssal"):
        self.owner = owner
        self.target = target
        self.value = value
        self.name = name
        self.description = description
        self.category = category

class Attack(Command):
    def __init__(self, owner=None, target=None, value=base_atk, name="Attack Command", 
    category="Basic Attack", is_raw=False):
        super().__init__(owner=owner, target=target, value=value, name=name, 
        category=category)
        self.is_raw = is_raw

    def execute(self):
        if(not self.target): return {"msg": "Target for Attack not selected"}
        try:
            actor_atk_stat = self.owner.atk_stat.value
            name = self.owner.name
        except AttributeError:
            actor_atk_stat = self.owner.owner.atk_stat.value
            name = self.owner.owner.name
        
        value_after_bonuses = actor_atk_stat - self.target.def_stat.value if not self.is_raw else 0
        final_value =  self.value + value_after_bonuses
        if final_value < 0: final_value = 0
        self.target.hp.value -= final_value
        
        return {
            "msg": f"{name} attacks {self.target.name} for {final_value} damage",
            "final_value": final_value,
            }

    # def undo(self):
    #     #or maybe just do a heal command?
    #     v = self.value + self.owner.atk_stat.value - self.target.def_stat.value
    #     hp = self.target.hp.value
    #     max_hp = self.target.max_hp.value
    #     self.target.hp.value = v + hp if hp + v <= max_hp else max_hp 

class Heal(Command):
    def __init__(self, owner=None, target=None, value=base_heal, name="Heal Command", 
    category="Healing"):
        super().__init__(owner=owner, target=target, value=value, name=name)

    def execute(self):
        if(not self.target):return {"msg": "Target for Heal not selected"}
        try:
            name = self.owner.name
        except AttributeError:
            name = self.owner.owner.name

        v = self.value
        hp = self.target.hp.value
        max_hp = self.target.max_hp.value
        self.target.hp.value = v + hp if hp + v <= max_hp else max_hp 
        return {"msg": f"{name} heals {v}, current hp: {self.target.hp.value}"}

    # def undo(self):
    #     self.target.hp.value -= self.value
    #     return {"msg": f"{self.owner.name} attacks {self.target.name} for {self.value} damage"}

class VampBite(Command):
    def __init__(self, owner=None, target=None, value=4, eff=0.5, name="Vampire Bite", 
    category="Special Attack"):
        super().__init__(owner=owner, target=target, value=value, name=name)
        self.eff = eff

    def execute(self):
        atk_result = Attack(owner=self.owner, target=self.target, value=self.value).execute()
        heal_value = int(atk_result["final_value"]*self.eff)
        Heal(owner=self.owner, target=self.owner, value=heal_value).execute()
        return {"msg": f"{self.owner.name} deals {atk_result['final_value']} and heals {heal_value}"}


# COMMANDS WITH BUFF/STATUSES
class CommandWithStatus(Command):
    def __init__(
    self, owner=None, target=None, value=0, timer=0, status_dict={}, 
    description="Whale Sage Command Description", name="Whale Sage Command", 
    category="Spiritual"):
        super().__init__(owner=owner, target=target, value=0 ,name=name, description=description, category=category)
        self.status_dict = status_dict
        self.timer = timer

    def execute(self):
        super().execute()

class SunCharge(CommandWithStatus):
    def __init__(self, owner=None, target=None, status_dict=con.SUN_CHARGE["status_dict"], name=con.SUN_CHARGE["name"], 
    description=con.SUN_CHARGE["description"], category=con.SUN_CHARGE["category"]):
        super().__init__(owner=owner, target=target, status_dict=status_dict, name=name, description=description, category=category)

    def execute(self):
        atk_stat = sts.AtkUp(target=self.target, status_dict={"atk_stat": self.status_dict["atk_stat"]}, timer=self.timer)
        def_stat = sts.DefUp(target=self.target, status_dict={"def_stat": self.status_dict["def_stat"]}, timer=self.timer)
        spd_stat = sts.SpdUp(target=self.target, status_dict={"spd_stat": self.status_dict["spd_stat"]},)
        self.target.statuses.add_status(atk_stat)
        self.target.statuses.add_status(def_stat)
        return {"msg": self.description}



#######################################################
class ToxicShot(CommandWithStatus):
    def __init__(self, owner=None, target=None, value=con.TOXIC_SHOT["value"], timer=con.TOXIC_SHOT["timer"], 
    status_dict=con.TOXIC_SHOT["status_dict"], name=con.TOXIC_SHOT["name"],
    category=con.TOXIC_SHOT["category"]):
        super().__init__(owner=owner, target=target, value=value, name=name, timer=timer, status_dict=status_dict)
        
    def execute(self):
        poison_status = sts.Poisoned(value=self.status_dict["poisoned"], timer=self.timer, target=self.target, owner=self.owner)
        self.target.statuses.add_status(poison_status)
        atk_results = Attack(target=self.target, owner=self.owner, value=self.value).execute()
        final_value = atk_results["final_value"]
        msg = atk_results["msg"]
        return {"msg": f"{self.target.name} takes {final_value} and is now poisoned for {self.timer} turns"}

class PowerUp(CommandWithStatus):
    def __init__(self, owner=None, target=None, value=2, timer=2, name="PowerUp"):
        super().__init__(owner=owner, target=target, value=value, name=name, timer=timer)

    def execute(self):
        atk_stat_status = sts.AtkUp(target=self.target, owner=self.owner)
        self.target.statuses.add_status(atk_stat_status)
        return {"msg":f"{self.target.name} gets powered up!"}

class Blessing(CommandWithStatus):
    def __init__(self, owner=None, target=None, value=2, timer=2, name="Blessing"):
        super().__init__(owner=owner, target=target, name=name )

    def execute(self):
        regen_status = sts.Regen(target=self.target, owner=self.owner)
        self.target.statuses.add_status(regen_status)
        return {"msg": f"{self.target.name} starts regenning"}
