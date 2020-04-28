import components.statuses as sts
import components.actors as actors
import constants.commands_cons as cons
from random import sample
from controllers.board_controller import add_actor_at_xy
from game_eye import GameEye

class CommandList():
    def __init__(self, **kwargs):
        self.base_list = []
        self.equip_list = []
        self.job_list = []
        self.list = []

    def add_command(self, command, category=""):
        for comm in self.list:
            if comm.name == command.name:
                print("Not able to add command cause it's already in the commands list")
        else:
            command.owner = self.owner
            self.list.append(command)
            if("base" in category):
                self.base_list.append(command)
            if("equip" in category):
                self.equip_list.append(command)
            if("job" in category):
                self.job_list.append(command)

    def remove_command(self, command): 
        command.owner = None  
        self.list.remove(command)

    def add_eye(self):
        self.game_eye = self.owner.game_eye

class Command():
    def __init__(self, **kwargs):
        self.name = kwargs.get('name', "Abyssal Lord Command")
        self.description = kwargs.get('description', "Abyssal Lord Command Description")
        self.category = kwargs.get('category', "Abyssal")
        
        self.owner = kwargs.get('owner', None)
        self.target = kwargs.get('target', None)
        self.target_xy = (-1, -1)

        self.value = kwargs.get('value', 0)
        self.timer = kwargs.get('timer', 0)
        self.is_raw = kwargs.get('is_raw', False)
        self.max_range = kwargs.get('max_range', 1)
        self.final_value = 0
        
        self.status_dict = kwargs.get('status_dict', {})
        self.command_dict = kwargs.get('command_dict', {})

        self.msg = kwargs.get("msg", "")
        self.msg_function = kwargs.get("msg_function", None)
        self.msg_args = kwargs.get("msg_args", None)

        self.game_eye = GameEye.instance()

    def execute(self):
        #this is still messy, do a more standardized way to separate 

        special_result = self.manage_special_status_or_commands()
        if(not special_result.get("should_continue", True)):
            return special_result

        params_status = {
            "owner": self.owner,
            "target": self.target,
            "value": self.value,
            "timer": self.timer,
        }
        params_commands = {**params_status, **{"command_dict": {}}}

        self.manage_statuses(params_status=params_status)

        execution_dict = self.manage_commands(params_commands=params_commands)

        if self.msg_function:
            return self.get_msg_dict()

        return {
            "msg": [action_result["msg"] for action_result in execution_dict.values()],
            "result": execution_dict,
        }

    def get_msg_dict(self):
        return {"msg": self.msg.format(*self.msg_function(*self.msg_args, self=self))}

    def manage_special_status_or_commands(self):
        owner_status_base_names = list(map(lambda x: x.base_name, self.owner.statuses.list))
        target_status_base_names = list(map(lambda x: x.base_name, self.target.statuses.list))

        if "stunned" in owner_status_base_names: 
            return {
                'msg': f"{self.owner.name} is stunned and can't move!",
                'valid_action': False,
                'result': {"attack": "no attack", "final_value": 0},
                'should_continue': False,
            }
        if "perfect_counter_stance" in target_status_base_names: 
            self.target = self.owner

        return {}

    def manage_statuses(self, params_status):
        statuses = {
            "atk_stat": sts.AtkUp(**params_status),
            "def_stat": sts.DefUp(**params_status),
            "spd_stat": sts.SpdUp(**params_status),
            "income_stat": sts.IncomeUp(**params_status),
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

    def manage_commands(self, params_commands):
        execution_dict = {}
        commands = {
            "attack": Attack(**params_commands),
            "heal": Heal(**params_commands),
        }
        for k, v in self.command_dict.items():
            action = commands.get(k)
            action.value = v if v else action.value
            execution_dict[k] = action.execute()

        return execution_dict

    def calculate_final_dmg_value(self, is_raw=False):
        actor_atk_stat = self.owner.atk_stat.value
        value_after_bonuses = actor_atk_stat - self.target.def_stat.value if not self.is_raw else 0
        final_value =  self.value + value_after_bonuses
        if final_value < 0: final_value = 0

        self.final_value = final_value

####################################
######### BASIC COMMANDS ###########
####################################

class Attack(Command):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


    def execute(self):
        result = super().execute()
        if not result.get("valid_action", True):
            return result

        self.calculate_final_dmg_value(is_raw=self.is_raw)
        self.deal_damage(self.final_value)

        if not self.msg_function: return

        return self.get_msg_dict()

    def deal_damage(self, damage):
        self.target.hp.value -= damage


class Heal(Command):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.heal_value = 0

    def execute(self):
        result = super().execute()
        if not result.get("valid_action", True):
            return result

        v = self.value
        hp = self.target.hp.value
        max_hp = self.target.max_hp.value
        self.target.hp.value = v + hp if hp + v <= max_hp else max_hp 

        self.heal_value = v
        if not self.msg_function: return

        return self.get_msg_dict()

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
        self.heal_value = 0
 
    def execute(self):
        result = super().execute()
        if not result.get("valid_action", True):
            return result
        Attack(owner=self.owner, target=self.target, value=self.value).execute()
        self.calculate_final_dmg_value()
        self.heal_value = int(self.final_value*self.eff)
        Heal(owner=self.owner, target=self.owner, value=self.heal_value).execute()
        return self.get_msg_dict()


####################################
######### KINGDOM COMMANDS #########
####################################

#SUN CHARGE HERE, very basic, doesn't need much stuff

class GoldenEgg(Command):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.original_status_dict = kwargs.get("status_dict")
        self.choices = []

    def execute(self):
        new_status_dict = self.choose_2_statuses()
        self.status_dict = new_status_dict
        super().execute()

    def choose_2_statuses(self):
        self.choices = sample(list(self.status_dict), k=2)
        
        new_status_dict = {
            self.choices[0]: self.original_status_dict[self.choices[0]],
            self.choices[1]: self.original_status_dict[self.choices[1]]
        }

        return new_status_dict

class Multiply(Command):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ratio = kwargs.get("ratio", 1/2)
    def execute(self):
        #maybe its better to use the create actor function
        parent = self.owner
        self.target = parent
        x, y = self.target_xy
        #Make this better! maybe use already existing "factory", or do a proper factory
        minion_stats = {
            "name": f"{parent.name}'s minion",
            "animal": f"small {parent.animal}",
            "letter": parent.letter.lower(),
            "kingdom": parent.kingdom,
            "hp": actors.Stat(value=int(parent.hp.value*self.ratio)),
            "atk_stat": actors.Stat(value=int(parent.atk_stat.value*(self.ratio**2))),
            "def_stat": actors.Stat(value=int(parent.def_stat.value*(self.ratio**2))),
            "spd_stat": actors.Stat(value=int(parent.spd_stat.value*self.ratio)),
            "income_stat": actors.Stat(value=int(parent.income_stat.value*self.ratio)),
            "commands": parent.commands.base_list,
            "x": x,
            "y": y,
            "game_eye": parent.game_eye.game
        }
        minion = actors.Actor(**minion_stats)
        self.game_eye.add_actor(minion)
        add_actor_at_xy(board=self.game_eye.get_board(), actor=minion, x=x, y=y)

####################################
######### EQUIPS COMMANDS ##########
####################################

#Slash (dagger) true dmg 10
#Shield Bash Attack (shield) stunned effect
#Rage (Cauldron)
#Perfect Counter
#Toxic Shot

####################################
######### STATUS COMMANDS ##########
####################################

#PowerUp
#DefenseUp
#SpeedUp

def instaciate_commands_dict():
    commands_dict = {
        #all/most of these could be made into a single command with different kwargs basically
        'attack': Attack(**cons.ATTACK),
        'heal': Heal(**cons.HEAL),
        'vamp_bite': VampBite(**cons.VAMP_BITE),

        'sun_charge': Command(**cons.SUN_CHARGE),
        'golden_egg': GoldenEgg(**cons.GOLDEN_EGG),
        'multiply': Multiply(**cons.MULTIPLY),
        
        'toxic_shot': Attack(**cons.TOXIC_SHOT),
        'rage': Command(**cons.RAGE_SOUP),
        'perfect_counter': Command(**cons.PERFECT_COUNTER),
        
        'power_up': Command(**cons.POWER_UP),
        'defense_up': Command(**cons.DEFENSE_UP),
        'speed_up': Command(**cons.SPEED_UP),
        'regen': Command(**cons.REGEN),
    }
    return commands_dict
