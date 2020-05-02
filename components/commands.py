import components.statuses as sts
import components.actors as actors
from random import sample
from controllers.board_controller import add_actor_at_xy
from game_eye import GameEye


class CommandList():
    def __init__(self, **kwargs):
        self.owner = kwargs.get("owner")
        self.base_list = []
        self.kingdom_list = []
        self.equip_list = []
        self.job_list = []
        self.list = []
        commands_ids = kwargs.get("commands_ids", [])
        self.init(commands_ids)
        
    def init(self, commands):
        for command in commands:
            self.add_command(command, "base")
        self.add_kingdom_command()

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
            if("kingdom" in category):
                self.kingdom_list.append(command)

    def remove_command(self, command, category=""): 
        command.owner = None  
        self.list.remove(command)
        if("base" in category):
            self.base_list.remove(command)
        if("equip" in category):
            self.equip_list.remove(command)
        if("job" in category):
            self.job_list.remove(command)
        if("kingdom" in category):
            self.kingdom_list.remove(command)

    def add_eye(self):
        self.game_eye = self.owner.game_eye

    def add_kingdom_command(self):
        kingdom = self.owner.kingdom
        command = {
            "mamalia": get_new_command_by_id(id="multiply"),
            "reptalia": get_new_command_by_id(id="sun_charge"),
            "aves": get_new_command_by_id(id="golden_egg"),
        }.get(kingdom)
        self.add_command(command, category="kingdom")

    def show_commands(self):
        commands_str = ''
        i = 1
        for command in self.list:
            commands_str = commands_str + f'({i}) {command.name} - '
            i += 1

        commands_str = commands_str[:-2] + '.'
        return commands_str

    def pass_turn(self):
        pass


class Command():
    def __init__(self, **kwargs):
        self.id = kwargs.get("id")
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
        
        from components.statuses import ComponentStatusList, get_new_statuses_by_ids
        self.statuses = ComponentStatusList()
        self.statuses.owner = self
        new_statuses_dict_list = kwargs.get("statuses_list", [])
        new_statuses_ids = list(map(lambda obj: obj["id"], new_statuses_dict_list))
        new_statuses = get_new_statuses_by_ids(ids_list=new_statuses_ids)
        self.statuses.add_statuses(statuses=new_statuses)

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

        params_commands = {
            "owner": self.owner,
            "target": self.target,
            "value": self.value,
            "timer": self.timer,
        }

        self.manage_statuses()

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
        # separate each into a self standing function
        # need to separate these functionallity into separate functions 
        owner_status_base_names, target_status_base_names = [], []
        if self.owner:
            owner_status_base_names = list(map(lambda x: x.base_name, self.owner.statuses.list))
        if self.target:
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

    def manage_statuses(self):
        from components.statuses import get_new_statuses_by_ids
        statuses_ids = list(map(lambda x: x.id, self.statuses.list))
        new_statuses_list = get_new_statuses_by_ids(ids_list=statuses_ids)
        self.add_statuses(new_statuses_list)

    def add_statuses(self, statuses):
        self.target.statuses.add_statuses_to_actor(statuses)

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
        actor_atk_stat = self.owner.atk_stat
        value_after_bonuses = actor_atk_stat - self.target.def_stat if not self.is_raw else 0
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

        self.deal_damage(self.final_value, is_raw=self.is_raw)
        if not self.msg_function: return
        return self.get_msg_dict()

    def deal_damage_to_target(self, damage, is_raw=True):
        self.calculate_final_dmg_value(is_raw=is_raw)
        self.target.hp_stat -= damage

class Heal(Command):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.heal_value = 0
        

    def execute(self):
        result = super().execute()
        if not result.get("valid_action", True):
            return result

        self.heal_damage(self, final_value)
        if not self.msg_function: return
        return self.get_msg_dict()

    def calculate_heal_damage(self, value):
        hp = self.target.hp_stat
        max_hp = self.target.max_hp_stat
        final_value = value + hp if hp + value <= max_hp else max_hp 
        return final_value

    def heal_damage(self, value):
        self.heal_value = self.calculate_final_heal_damage(value)
        self.target.hp += self.heal_value

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
        self.original_statuses_list = self.statuses.list

    def execute(self): 
        self.statuses.list = sample(self.original_statuses_list, k=2)
        super().execute()        

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
            "hp_stat": int(parent.hp_stat*self.ratio),
            "atk_stat": int(parent.atk_stat*(self.ratio**2)),
            "def_stat": int(parent.def_stat*(self.ratio**2)),
            "spd_stat": int(parent.spd_stat*self.ratio),
            "income_stat": int(parent.income_stat*self.ratio),
            "commands": parent.commands.base_list,
            "x": x,
            "y": y,
            "game_eye": parent.game_eye.game
        }
        minion = actors.Actor(**minion_stats)
        self.game_eye.add_actor(minion)
        add_actor_at_xy(board=self.game_eye.get_board(), actor=minion, x=x, y=y)

## others
# Toxic Shot

####################################
######### EQUIPS COMMANDS ##########
####################################

#Slash (dagger) true dmg 10
#Shield Bash Attack (shield) stunned effect
#Rage (Cauldron)
#Zulu Shot

####################################
######### JOBS COMMANDS ############
####################################

#Perfect Counter

class CopyCat(Command):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.has_stolen = False
        self.stolen_command = None

    def execute(self):
        copied_command = None
        if self.has_stolen:
            self.name = "Steal"
            self.has_stolen = False
            self.owner.commands.remove_command(self.stolen_command)
            self.msg = f"{self.owner} forgets previous command!"
        else:
            self.name = "Forget"
            self.has_stolen = True
            target = self.target
            if target.job:
                copied_command = sample(target.commands.job_list, k=1)[0]
            elif target.equip:
                copied_command = sample(target.commands.equip_list, k=1)[0]
            else:
                copied_command = target.commands.base_list[-1]
            copied_command = get_new_command_by_id(id=copied_command.id)
            self.stolen_command = copied_command
            self.owner.commands.add_command(copied_command)
            self.msg = f"{self.owner.name} copies {copied_command.name} from {target.name}!"

        return {"msg": self.msg}

class Mixn(Command):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def execute(self):
        if not self.target.equip:
            return {"msg": "Target doesn't have an equip to mix with"}
        from components.elements import get_new_element_by_id
        element = get_new_element_by_id(id="fire")
        self.target.equip.add_element(element)
        
        return {"msg": f"{self.owner.name} adds {element.name} element to a {self.target.equip.name}"}

####################################
######### STATUS COMMANDS ##########
####################################

#PowerUp
#DefenseUp
#SpeedUp
#IncomeUp
#MaxHpUp

def instaciate_commands_dict(**kwargs):
    '''
    cons content
    {
        "name": ,
        "timer": , #only for commands with statuses_list
        "value": , #only for commands that deal/heal <value> hp
        "description": ,
        "category": ,
        "eff" : , #for now only for VampBite(), it shows the efficiency of the vampire bite heal
        "is_raw": , # default is False, only valid for commands that use Attack()
        # if is_raw is false it means the damage dealt will be "pure" (desregarding atk and def bonuses)
        "statuses_list": { #optional if command has stat buffs
            <status_name>: status_value
        },
        "command_dict": {
            <command_name>: command_value
        },
        "max_range": 1,
    }
    '''
    import constants.commands_cons as cons
    commands_dict = {
        #all/most of these could be made into a single command with different kwargs basically
        'attack': Attack(**{**cons.ATTACK, **kwargs}),
        'heal': Heal(**{**cons.HEAL, **kwargs}),
        'vamp_bite': VampBite(**{**cons.VAMP_BITE, **kwargs}),

        'sun_charge': Command(**{**cons.SUN_CHARGE, **kwargs}),
        'golden_egg': GoldenEgg(**{**cons.GOLDEN_EGG, **kwargs}),
        'multiply': Multiply(**{**cons.MULTIPLY, **kwargs}),
        
        'true_slash': Attack(**{**cons.DAGGER_ATTACK, **kwargs}),
        'toxic_shot': Attack(**{**cons.TOXIC_SHOT, **kwargs}),
        'paralize_shot': Attack(**{**cons.PARALIZE_SHOT, **kwargs}),
        'rage': Command(**{**cons.RAGE_SOUP, **kwargs}),
        'shield_bash': Attack(**{**cons.SHIELD_BASH, **kwargs}),

        'perfect_counter': Command(**{**cons.PERFECT_COUNTER, **kwargs}),
        'copy_cat': CopyCat(**{**cons.COPY_CAT, **kwargs}),
        'mixn': Mixn(**{**cons.MIXN, **kwargs}),

        'power_up': Command(**{**cons.POWER_UP, **kwargs}),
        'defense_up': Command(**{**cons.DEFENSE_UP, **kwargs}),
        'speed_up': Command(**{**cons.SPEED_UP, **kwargs}),
        # 'income_up': Command(**{**cons.INCOME_UP, **kwargs}),
        # 'max_hp_up': Command(**{**cons.MAX_HP_UP, **kwargs}),
        'regen': Command(**{**cons.REGEN, **kwargs}),
    }
    return commands_dict

def get_new_command_by_id(**kwargs):
    id = kwargs.get("id")
    commands = instaciate_commands_dict(**kwargs)
    
    return commands.get(id)
