import statuses as sts
import commands_constants as con

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
    def __init__(self, owner, target, value, name="Abyssal Lord Command", description="Abyssal Lord Command Description", category="Abyssal"):
        self.owner = owner
        self.target = target
        self.value = value
        self.name = name
        self.description = description
        self.category = category

class Attack(Command):
    def __init__(self, owner, target, value, name="Attack Command"):
        super().__init__(owner=owner, target=target, value=value, name=name)

    def execute(self):
        final_value = self.owner.atk_stat.value + self.value - self.target.def_stat.value
        if final_value <0: final_value = 0
        self.target.hp.value -= final_value
        
        return {
            "msg": f"{self.owner.name} attacks {self.target.name} for {final_value} damage",
            "final_value": final_value,
            }

    # def undo(self):
    #     #or maybe just do a heal command?
    #     v = self.value + self.owner.atk_stat.value - self.target.def_stat.value
    #     hp = self.target.hp.value
    #     max_hp = self.target.max_hp.value
    #     self.target.hp.value = v + hp if hp + v <= max_hp else max_hp 

class Heal(Command):
    def __init__(self, owner, target, value, name="Heal Command"):
        super().__init__(owner=owner, target=target, value=value, name=name)

    def execute(self):
        #or maybe just do an attack command?
        v = self.value
        hp = self.target.hp.value
        max_hp = self.target.max_hp.value
        self.target.hp.value = v + hp if hp + v <= max_hp else max_hp 
        return {"msg": f"{self.owner.owner.name} heals {v}, current hp: {self.target.hp.value}"}

    # def undo(self):
    #     self.target.hp.value -= self.value
    #     return {"msg": f"{self.owner.name} attacks {self.target.name} for {self.value} damage"}

class VampBite(Command):
    def __init__(self, owner, target, value=4, eff=0.5, name="VampBite Command"):
        super().__init__(owner=owner, target=target, value=value, name=name)
        self.eff = eff

    def execute(self):
        atk_result = Attack(owner=self.owner, target=self.target, value=self.value).execute()
        heal_value = int(atk_result["final_value"]*self.eff)
        Heal(owner=self.owner, target=self.owner, value=heal_value).execute()
        return {"msg": f"{self.owner.name} deals {atk_result['final_value']} and heals {heal_value}"}


# COMMANDS WITH BUFF/STATUSES
class CommandWithStatus(Command):
    def __init__(self, timer, owner, target, attr_dict={}, description="Whale Sage Command Description", name="Whale Sage Command", category="Spiritual"):
        super().__init__(owner=owner, target=target, value=0 ,name=name, description=description, category=categoty)
        self.attr_dict = attr_dict
        self.timer = timer

    def execute(self):
        super().execute()

class SunCharge(CommandWithStatus):
    def __init__(self, owner=None, target=None, attr_dict=con.SUN_CHARGE["attr_dict"], name=con.SUN_CHARGE["name"], 
                    description=con.SUN_CHARGE["description"], category=con.SUN_CHARGE["category"]):
        super().__init__(owner=owner, target=target, attr_dict=attr_dict, name=name, description=description, category=category)

    def execute(self):
        atk_up = sts.AtkUp(value=self.attr_dict["atk_stat"], timer=self.timer)
        def_up = sts.DefUp(value=self.attr_dict["def_stat"], timer=self.timer)
        self.target.statuses.add_status(atk_up)
        self.target.statuses.add_status(def_up)
        return {"msg": self.description}



#######################################################
class ToxicShot(CommandWithStatus):
    def __init__(self, owner, target, value, status_value, status_timer, name="ToxicShot Command"):
        super().__init__(owner=owner, target=target, value=value, name=name, 
                        status_value=status_value, status_timer=status_timer)

    def execute(self):
        poison_status = sts.Poisoned(value=self.status_value, timer=self.status_timer, target=self.target, owner=self.owner)
        self.target.statuses.add_status(poison_status)
        return {"msg": f"{self.target.name} takes {self.value} and is now poisoned for {self.status_timer} turns"}

class PowerUp(CommandWithStatus):
    def __init__(self, owner, target, name="PowerUp Command"):
        super().__init__(owner=owner, target=target, value=value, name=name, 
                        status_value=status_value, status_timer=status_timer)

    def execute(self):
        atk_up_status = sts.AtkUp(timer=self.status_timer, target=self.target, owner=self.owner)
        self.target.statuses.add_status(atk_up_status)
        return {"msg":f"{self.target.name} gets powered up!"}

class Blessing(CommandWithStatus):
    def __init__(self, owner, target):
        super().__init__(owner=owner, target=target, name=name, 
                       )

    def execute(self):
        regen_status = sts.Regen(value=self.status_value, target=self.target, owner=self.owner, timer=self.status_timer)
        self.target.statuses.add_status(regen_status)
        return {"msg": f"{self.target.name} starts regenning"}
