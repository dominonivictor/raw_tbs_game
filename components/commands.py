import components.statuses as sts
import components.actors as actors
from random import sample
from controllers.board_controller import add_actor_at_xy
from game_eye import GameEye


class Command:
    def __init__(self, **kwargs):
        # I think this is getting wayyyyy too big... maybe separate what is not needed
        # and leave it only for the children specif commands that need it...?
        self.id = kwargs.get("id")
        self.name = kwargs.get("name", "Abyssal Lord Command")
        self.description = kwargs.get("description", "Abyssal Lord Command Description")
        self.category = kwargs.get("category", "Abyssal")

        self.owner = kwargs.get("owner", None)
        self.target = kwargs.get("target", None)
        self.target_xy = (-1, -1)
        self.target_pos = (0, 0)
        self.target_x = 0
        self.target_y = 0

        self.value = kwargs.get("value", 0)
        self.timer = kwargs.get("timer", 0)
        self.is_raw = kwargs.get("is_raw", False)
        self.max_range = kwargs.get("max_range", 1)
        self.final_value = 0

        self.raw_statuses_ids = kwargs.get("statuses_list", [])
        from components.statuses import ComponentStatusList

        self.statuses = ComponentStatusList(
            owner=self, raw_statuses_ids=self.raw_statuses_ids
        )

        self.command_dict = kwargs.get("command_dict", {})
        self.msg = kwargs.get("msg", "")
        self.msg_function = kwargs.get("msg_function", None)
        self.msg_args = kwargs.get("msg_args", None)

        self.game_eye = GameEye.instance()

    def execute(self):
        # this is still messy, do a more standardized way to separate

        special_result = self.manage_special_status_or_commands()
        if not special_result.get("should_continue", True):
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
        from functions.special_status_functions import special_status_handler

        response = special_status_handler(self)
        return response

    def manage_statuses(self):
        from components.statuses import get_new_statuses_by_ids

        new_statuses_list = get_new_statuses_by_ids(status_list=self.raw_statuses_ids)
        self.add_statuses_ownership(statuses=new_statuses_list)
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
        actor_atk_stat = self.owner.get_atk()
        bonuses = actor_atk_stat - self.target.get_def() if not is_raw else 0
        final_value = self.value + bonuses
        if final_value < 0:
            final_value = 0

        self.final_value = final_value
        return final_value

    def add_statuses_ownership(self, statuses: list):
        for status in statuses:
            status.set_owner(owner=self.owner)
            status.set_target(target=self.target)

    def set_target(self, target):
        self.target = target

    def get_value(self):
        return self.value

    def get_timer(self):
        return self.timer

    def get_statuses_values(self, pos=None):
        if type(pos) is int:
            return self.statuses.list[pos].value
        return list(map(lambda x: x.value, self.statuses.list))

    def get_target_x(self):
        return self.target_x

    def get_target_y(self):
        return self.target_y

    def set_target_x(self, x):
        self.target_x = x

    def set_target_y(self, y):
        self.target_y = y

    def get_target_pos(self):
        return self.target_pos

    def set_target_pos(self, pos):
        x, y = pos
        self.set_target_x(x)
        self.set_target_y(y)
        self.target_pos = (self.target_x, self.target_y)


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
        self.deal_damage_to_target(self.final_value, is_raw=self.is_raw)
        if not self.msg_function:
            return
        return self.get_msg_dict()

    def deal_damage_to_target(self, damage, is_raw=True):
        self.final_value = self.calculate_final_dmg_value(is_raw=is_raw)
        self.target.take_damage(value=self.final_value)


class Heal(Command):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.heal_value = 0

    def execute(self):
        result = super().execute()
        if not result.get("valid_action", True):
            return result

        self.heal_damage(self.value)
        if not self.msg_function:
            return
        return self.get_msg_dict()

    def heal_damage(self, value):
        self.target.heal_damage(value)


class VampBite(Command):
    """
    wanted to make vampbite part of customizable stuff but maybe i can leave it as a base skill...
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.eff = kwargs.get("eff", 0)
        self.heal_value = 0

    def execute(self):
        result = super().execute()
        if not result.get("valid_action", True):
            return result
        Attack(owner=self.owner, target=self.target, value=self.value).execute()
        self.calculate_final_dmg_value()
        self.heal_value = int(self.final_value * self.eff)
        Heal(owner=self.owner, target=self.owner, value=self.heal_value).execute()
        return self.get_msg_dict()


####################################
######### KINGDOM COMMANDS #########
####################################

# SUN CHARGE HERE, very basic, doesn't need much stuff


class GoldenEgg(Command):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.original_raw_ids = self.raw_statuses_ids
        self.original_statuses_list = self.statuses.list

    def execute(self):
        self.raw_statuses_ids = sample(self.original_raw_ids, k=2)
        super().execute()


class Multiply(Command):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ratio = kwargs.get("ratio", 1 / 2)

    def execute(self):
        # maybe its better to use the create actor function
        parent = self.owner
        self.target = parent
        x, y = self.target_xy
        # Make this better! maybe use already existing "factory", or do a proper factory
        # too much processing inside the dictionary... extract everything
        minion_stats = {
            "name": f"{parent.name}'s minion",
            "animal": f"small {parent.animal}",
            "letter": parent.letter.lower(),
            "kingdom": parent.kingdom,
            "hp_stat": int(parent.get_hp() * self.ratio),
            "atk_stat": int(parent.get_atk() * (self.ratio ** 2)),
            "def_stat": int(parent.get_def() * (self.ratio ** 2)),
            "spd_stat": int(parent.get_spd() * self.ratio),
            "income_stat": int(parent.get_inc() * self.ratio),
            "commands": parent.commands.base_list,
            "x": x,
            "y": y,
            "game_eye": parent.game_eye.game,
        }
        minion = actors.Actor(**minion_stats)
        self.game_eye.add_actor(minion)
        # communicates too much with board and stuff... is there a workaround?
        add_actor_at_xy(board=self.game_eye.get_board(), actor=minion, x=x, y=y)

        return self.get_msg_dict()


## others
# Toxic Shot

####################################
######### EQUIPS COMMANDS ##########
####################################

# Slash (dagger) true dmg 10
# Shield Bash Attack (shield) stunned effect
# Rage (Cauldron)
# Zulu Shot

####################################
######### JOBS COMMANDS ############
####################################

# Perfect Counter


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
            self.msg = (
                f"{self.owner.name} copies {copied_command.name} from {target.name}!"
            )

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

        return {
            "msg": f"{self.owner.name} adds {element.name} element to a {self.target.equip.name}"
        }


####################################
######### STATUS COMMANDS ##########
####################################

# PowerUp
# DefenseUp
# SpeedUp
# IncomeUp
# MaxHpUp


####################################
######### AOE COMMANDS #############
####################################
from functions.grid_patterns import create_grid_coords


class AOE(Command):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.aoe_size = kwargs.get("aoe_size", 1)
        self.tile_pattern = create_grid_coords(size=self.aoe_size)

    def execute(self):
        target_list = []
        for tile_x, tile_y in self.tile_pattern:
            target_x = self.get_target_x() + tile_x
            target_y = self.get_target_y() + tile_y
            if self.game_eye.has_actor_on_xy(target_x, target_y):
                target = self.game_eye.get_actor_on_xy(target_x, target_y)
                target_list.append(target.name)
                self.set_target(target)
                super().execute()

        msg = f"{target_list} took dmg to waterball"

        return {"msg": msg}


def instaciate_commands_dict(**kwargs):
    """
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
    """
    import constants.commands_cons as cons

    commands_dict = {
        # all/most of these could be made into a single command with different kwargs basically
        "attack": Attack(**{**cons.ATTACK, **kwargs}),
        "heal": Heal(**{**cons.HEAL, **kwargs}),
        "vamp_bite": VampBite(**{**cons.VAMP_BITE, **kwargs}),
        "wind_blow": Attack(**{**cons.WIND_BLOW, **kwargs}),
        "poison_tail": Attack(**{**cons.POISON_TAIL, **kwargs}),
        "sun_charge": Command(**{**cons.SUN_CHARGE, **kwargs}),
        "golden_egg": GoldenEgg(**{**cons.GOLDEN_EGG, **kwargs}),
        "multiply": Multiply(**{**cons.MULTIPLY, **kwargs}),
        "perfect_counter": Command(**{**cons.PERFECT_COUNTER, **kwargs}),
        "copy_cat": CopyCat(**{**cons.COPY_CAT, **kwargs}),
        "mixn": Mixn(**{**cons.MIXN, **kwargs}),
        "true_slash": Attack(**{**cons.DAGGER_ATTACK, **kwargs}),
        "toxic_shot": Attack(**{**cons.TOXIC_SHOT, **kwargs}),
        "paralize_shot": Attack(**{**cons.PARALIZE_SHOT, **kwargs}),
        "rage": Command(**{**cons.RAGE_SOUP, **kwargs}),
        "shield_bash": Attack(**{**cons.SHIELD_BASH, **kwargs}),
        "power_up": Command(**{**cons.POWER_UP, **kwargs}),
        "defense_up": Command(**{**cons.DEFENSE_UP, **kwargs}),
        "speed_up": Command(**{**cons.SPEED_UP, **kwargs}),
        # 'income_up': Command(**{**cons.INCOME_UP, **kwargs}),
        # 'max_hp_up': Command(**{**cons.MAX_HP_UP, **kwargs}),
        "regen": Command(**{**cons.REGEN, **kwargs}),
        "waterball": AOE(**{**cons.WATERBALL, **kwargs}),
        "wave_money_bag": AOE(**{**cons.WAVE_MONEY_BAG, **kwargs}),
    }
    return commands_dict


def get_new_command_by_id(**kwargs):
    id_ = kwargs.get("id")
    commands = instaciate_commands_dict(**kwargs)

    return commands.get(id_)


def get_new_commands_by_ids(command_ids: list) -> list:

    return [get_new_command_by_id(id=c) for c in command_ids]
