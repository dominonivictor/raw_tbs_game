import components.statuses as sts
import constants.commands_cons as con

class CommandList():
    def __init__(self):
        self.list = []

    def add_command(self, command):
        for comm in self.list:
            if comm.name == command.name:
                print("Not able to add command cause it's already in the commands list")
        else:
            command.owner = self.owner
            self.list.append(command)

    def update_command(self, command_name, attrs_dict):
        # for comm in self.list:
        #     if comm.name == command_name:
        pass            

    def remove_command(self, command): 
        command.owner = None  
        self.list.remove(command)

class Command():
    def __init__(self, **kwargs):
        self.name = kwargs.get('name', "Abyssal Lord Command")
        self.description = kwargs.get('description', "Abyssal Lord Command Description")
        self.category = kwargs.get('category', "Abyssal")
        self.owner = kwargs.get('owner', None)
        self.target = kwargs.get('target', None)
        self.value = kwargs.get('value', 0)
        self.timer = kwargs.get('timer', 0)
        self.is_raw = kwargs.get('is_raw', False)
        self.max_range = kwargs.get('max_range', 1)
        self.status_dict = kwargs.get('status_dict', {})
        self.command_dict = kwargs.get('command_dict', {})


    def execute(self):
        #probably start separating all this mess into smaller functions

        owner_status_base_names = list(map(lambda x: x.base_name, self.owner.statuses.list))
        target_status_base_names = list(map(lambda x: x.base_name, self.target.statuses.list))

        if "stunned" in owner_status_base_names: 
            return {
                'msg': f"{self.owner.name} is stunned and can't move!",
                'valid_action': False,
                'result': {"attack": "no attack", "final_value": 0}
            }
        if "perfect_counter_stance" in target_status_base_names: 
            self.target = self.owner

        
        execution_dict = {}
        params_status = {
            "owner": self.owner,
            "target": self.target,
            "value": self.value,
            "timer": self.timer,
        }
        params_commands = {**params_status, **{"command_dict": {}}}

        commands = {
            "attack": Attack(**params_commands),
            "heal": Heal(**params_commands),
        }

        #need to add status_dict[attr] to each individually

        statuses = {
            "atk_stat": sts.AtkUp(**params_status),
            "def_stat": sts.DefUp(**params_status),
            "spd_stat": sts.SpdUp(**params_status),
            "regen": sts.Regenerating(**params_status),
            "poisoned": sts.Poisoned(**params_status),
            "burned": sts.Burned(**params_status),
            "stunned": sts.Stunned(**params_status),
            "perfect_counter_stance": sts.PerfectCounterStance(**params_status),
        }

        for k, v in self.status_dict.items():
            status = statuses.get(k)
            if self.target:
                status.target = self.target
            status.status_dict[k] = v 
            self.target.statuses.add_status(status)

        for k, v in self.command_dict.items():
            action = commands.get(k)
            action.value = v if v else action.value
            execution_dict[k] = action.execute()

        return {
            "msg": [action_result["msg"] for action_result in execution_dict.values()],
            "result": execution_dict,
        }

class Attack(Command):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def execute(self):
        result = super().execute()

        if not result.get("valid_action", True):
            return result

        name = self.owner.name
    
        final_value = self.calculate_final_dmg_value(is_raw=self.is_raw)
        self.deal_damage(final_value)
        
        return {
            "msg": f"{name} attacks {self.target.name} for {final_value} damage",
            "final_value": final_value,
            }

    def deal_damage(self, damage):
        self.target.hp.value -= damage

    def calculate_final_dmg_value(self, is_raw=False):
        actor_atk_stat = self.owner.atk_stat.value
        value_after_bonuses = actor_atk_stat - self.target.def_stat.value if not self.is_raw else 0
        final_value =  self.value + value_after_bonuses
        if final_value < 0: final_value = 0

        return final_value

    # def undo(self):
    #     #or maybe just do a heal command?
    #     v = self.value + self.owner.atk_stat.value - self.target.def_stat.value
    #     hp = self.target.hp.value
    #     max_hp = self.target.max_hp.value
    #     self.target.hp.value = v + hp if hp + v <= max_hp else max_hp 

class Heal(Command):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def execute(self):
        result = super().execute()
        if not result.get("valid_action", True):
            return result
        if(not self.target):return {"msg": "Target for Heal not selected, lost turn! :P"}
        try:
            name = self.owner.name
        except AttributeError:
            print(">>>>>>>>>>>>>>>YOU SHOULDN'T BE HERE (inside Heal.execute exception)")
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
    '''
    wanted to make vampbite part of customizable stuff but maybe i can leave it as a base skill...
    '''
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.eff = kwargs.get('eff', 0)
 
    def execute(self):
        result = super().execute()
        if not result.get("valid_action", True):
            return result
        atk_result = Attack(owner=self.owner, target=self.target, value=self.value).execute()
        heal_value = int(atk_result["final_value"]*self.eff)
        Heal(owner=self.owner, target=self.owner, value=heal_value).execute()
        return {"msg": f"{self.owner.name} deals {atk_result['final_value']} and heals {heal_value}"}


# COMMANDS WITH BUFF/STATUSES

# class CommandWithStatus(Command):
#     '''
#     I think this is gone now...
#     '''
#     def __init__(
#     self, owner=None, target=None, value=0, timer=0, status_dict={}, 
#     description="Whale Sage Command Description", name="Whale Sage Command", 
#     category="Spiritual", command_dict={}, is_raw=False):
#         super().__init__(owner=owner, target=target, value=value ,name=name, description=description, 
#         category=category, timer=timer, status_dict=status_dict, command_dict=command_dict, is_raw=is_raw)

#     def execute(self):
#         super().execute()

class SunCharge(Command):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def execute(self):
        super().execute()
        return {"msg": self.description}

#######################################################
class ToxicShot(Command):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
    def execute(self):
        result = super().execute()
        atk_results = result["result"]["attack"]
        final_value = atk_results["final_value"]
        return {"msg": f"{self.target.name} takes {final_value} and is now poisoned for {self.timer} turns"}

class PowerUp(Command):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def execute(self):
        super().execute()
        return {"msg":f"{self.target.name} gets powered up!"}

class Regen(Command):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def execute(self):
        super().execute()
        return {"msg": f"{self.target.name} starts regenning"}

class Rage(Command):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def execute(self):
        super().execute()
        return {"msg": f"{self.target.name} is enraged (ATK +, DEF -)"}

class PerfectCounter(Command):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def execute(self):
        super().execute()
        return {"msg": f"{self.target.name} is ready for anything!"}