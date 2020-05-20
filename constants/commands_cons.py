default = None
base_atk = 3
base_heal = 4
base_buff = 2
buff_plus = 1
buff_minus = -1
vamp_bite_eff = 0.5
short_timer = 2 # 1 round
mid_timer = 3 # 2 rounds
long_timer = 4 # 3 rounds

def get_attrs(*args, self=None):
    if not self: return "Nothing to say"

    result = []

    for string in args:
        obj, attr = string.split(" ")
        aimed_obj = {
            "owner": self.owner,
            "target": self.target,
            "command": self,
            "self": self,
        }.get(obj)

        aimed_attr = {
            "name": aimed_obj.name,
            "value": aimed_obj.value if hasattr(aimed_obj, "value") else None,
            "final_value": aimed_obj.final_value if hasattr(aimed_obj, "final_value") else None,
            "heal_value": aimed_obj.heal_value if hasattr(aimed_obj, "heal_value") else None,
            "choices": aimed_obj.choices if hasattr(aimed_obj, "choices") else None,
            "timer": aimed_obj.timer if hasattr(aimed_obj, "timer") else None,
        }.get(attr)

        result.append(aimed_attr)   
        
    return result

####################################
######### BASIC COMMANDS ###########
####################################

ATTACK = {
    "id": "attack",
    "name": "Punch",
    "value": base_atk, #only for commands that deal/heal <value> hp
    "description": "Gives a good old punch to the face",
    "category": "Basic Attack",  
    "is_raw": False,
    "max_range": 1,
    "msg": "{} attacks {} for {} damage!",
    "msg_function": get_attrs,
    "msg_args": ["owner name", "target name", "self final_value"],  
}

HEAL = {
    "id": "heal",
    "name": "Healing Salve",
    "value": base_heal, #only for commands that deal/heal <value> hp
    "description": "Gives a healing salve to the target",
    "category": "Basic Heal",  
    "max_range": 2, 
    "msg": "{} heals {} for {} hp!",
    "msg_function": get_attrs,
    "msg_args": ["owner name", "target name", "self heal_value"], 
}

VAMP_BITE = {
    "id": "vamp_bite",
    "name": "Vampire's Bite",
    "value": base_atk, #only for commands that deal/heal <value> hp
    "description": "Attacks the target healing for half the amount",
    "category": "Special Attack/Attack and Heal?",
    "eff": vamp_bite_eff,
    "is_raw": False, # default is False, only valid for commands that use Attack()
    # if is_raw is false it means the damage dealt will be "pure" (desregarding atk and def bonuses)
    "max_range": 1,
    "msg": "{} deals {} to {} and heals for {} hp!",
    "msg_function": get_attrs,
    "msg_args": ["owner name", "self final_value", "target name", "self heal_value"],
}

####################################
######### KINGDOM COMMANDS #########
####################################

SUN_CHARGE = {
    "id": "sun_charge",
    "name": "Sun Charge",
    "statuses_list": [
        {"id": "atk_up", "value": 1, "timer": mid_timer,},
        {"id": "def_up", "value": 1, "timer": mid_timer,},
        {"id": "spd_up", "value": 1, "timer": mid_timer,},
    ],
    "timer": mid_timer,
    "description": "Sun Charge increases all stats by 1 for 1 turn.",
    "category": "Greater Buff",
    "max_range": 2,
    "msg": "{} increases atk, def, spd by 1 for 2 turns",
    "msg_function": get_attrs,
    "msg_args": ["owner name"],
}

GOLDEN_EGG = {
    "id": "golden_egg",
    "name": "Golden Egg",
    "timer": 2, #only for commands with statuses_list
    "description": "Grants 2 random bonuses for 1 turn",
    "category": "Greater Buff",
    "statuses_list": [
        {"id": "atk_up", "value": 2, "timer": 2,},
        {"id": "def_up", "value": 2, "timer": 2,},
        {"id": "spd_up", "value": 2, "timer": 2,},
        {"id": "income_up", "value": 2, "timer": 2,},
    ],                                   
                                         
    "max_range": 1,
    "msg": "{} gets buffed on {} by 2? for 1 turn",
    "msg_function": get_attrs,
    "msg_args": ["owner name", "self choices"],
}

MULTIPLY = {
    "id": "multiply",
    "name": "Multiply",
    "description": "Creates a minion to fight for you",
    "category": "Summon",
    "max_range": 2,
    "command_dict": {
        "attack": 10
    },
    "msg": "{} gives life to a smaller version of thyself",
    "msg_function": get_attrs,
    "msg_args": ["owner name"],
}

####################################
######### EQUIPS COMMANDS ##########
####################################

DAGGER_ATTACK = {
    "id": "true_slash",
    "name": "True Slash",
    "value": 10, #only for commands that deal/heal <value> hp
    "description": "True dmg dealing dagger",
    "category": "Basic Attack",  
    "is_raw": True,
    "max_range": 1,
    "msg": "{} pierces {} for {} damage",
    "msg_function": get_attrs,
    "msg_args": ["owner name", "target name", "self final_value"],

}

TOXIC_SHOT = {
    "id": "toxic_shot",
    "name": "Toxic Shot",
    "statuses_list": [
        {"id": "poisoned", "value": 2, "timer": mid_timer,},
    ],
    "timer": mid_timer,
    "value": 2,
    "description": "Shoots target and poisons for 3 turns",
    "category": "Attack and DoT",
    "max_range": 3,
    "msg": "{} shots {} for {} damage and {} is poisoned for {} turns",
    "msg_function": get_attrs,
    "msg_args": ["owner name", "target name", "self final_value", "target name", "self timer"],
}

SHIELD_BASH = {
    "id": "shield_bash",
    "name": "Shield Bash",
    "value": 3, #only for commands that deal/heal <value> hp
    "description": "Bashes oponnent, leaving him stunned",
    "category": "Basic Attack",
    "statuses_list": [
        {"id": "stunned", "value": 2, "timer": 2},
    ],
    "is_raw": False,
    "max_range": 1,
    "msg": "{} hits and stuns {} for {} damage",
    "msg_function": get_attrs,
    "msg_args": ["owner name", "target name", "self final_value"],
}

RAGE = {
    "id": "rage",
    "name": "Rage",
    "timer": 2, #only for commands with statuses_list
    "description": "Someone is mad",
    "category": "Major Buff",
    "statuses_list": [
        {"id": "atk_up", "value": 3, "timer": 2,},
        {"id": "def_up", "value": -2, "timer": 2,},
    ],
    "max_range": 3,
    "msg": "{} is enraged! (+ATK, -DEF)",
    "msg_function": get_attrs,
    "msg_args": ["owner name"],
}

RAGE_SOUP = {
    **RAGE,
    'name': 'Rage Soup'
}


#toxic and zaraba should be the same, probably remove this or rework it
PARALIZE_SHOT = {
    "id": "paralize_shot",
    "name": "Paralisis Shot",
    "statuses_list": [
        {"id": "stunned", "timer": short_timer},
    ],
    # "command_dict": {
    #     "attack": base_atk - 1,
    # },
    "timer": short_timer,
    "value": base_atk - 1,
    "description": "Shoots target and stuns for 2 turns",
    "category": "Attack and DoT",
    "max_range": 3,
    "msg": "{} shots {} for {} damage and stuns {} for {} turns",
    "msg_function": get_attrs,
    "msg_args": ["owner name", "target name", "self final_value", "target name", "self timer"],
}

####################################
######### JOBS COMMANDS ############
####################################

PERFECT_COUNTER = {
    "id": "perfect_counter",
    "name": "Perfect Counter",
    "timer": 2, #only for commands with statuses_list
    "description": "Full Counter",
    "category": "Major Buff",
    "statuses_list": [
        {"id": "perfect_counter_stance", "timer": 2,},
    ],
    "max_range": 0,
    "msg": "{} takes a defensive stance",
    "msg_function": get_attrs,
    "msg_args": ["owner name"],
}

COPY_CAT = {
    "id": "copy_cat",
    "name": "Copy Cat",
    "description": "Copies target command",
    "category": "Utility",
    "max_range": 3,
}

MIXN = {
    "id": "mixn",
    "name": "Mixn",
    "description": "Adds element to target that has an equip",
    "category": "Utility",
    "max_range": 3,
}

####################################
######### STATUS COMMANDS ##########
####################################

POWER_UP = {
    "id": "power_up",
    "name": "Power Up",
    "statuses_list": [
        {"id": "atk_up", "value": 2, "timer": 2,},
    ],
    "timer": 2, #only for commands with statuses_list
    "description": "Owner gets a bonus for its attack for 2 for 1 turn",
    "category": "Minor Buff",
    # if is_raw is false it means the damage dealt will be "pure" (desregarding atk and def bonuses)
    "max_range": 2,
    "msg": "{} gets powered up for {} turns",
    "msg_function": get_attrs,
    "msg_args": ["target name", "self timer"],
}

DEFENSE_UP = {
    "id": "defense_up",
    "name": "Defense Up",
    "statuses_list": [
        {"id": "def_up", "value": 2, "timer": 2,},
    ],
    "timer": 2, #only for commands with statuses_list
    "description": "Owner gets a bonus for its defense for 2 for 1 turn",
    "category": "Minor Buff",
    # if is_raw is false it means the damage dealt will be "pure" (desregarding atk and def bonuses)
    "max_range": 2,
    "msg": "{} strenghtens defenses for {} turns",
    "msg_function": get_attrs,
    "msg_args": ["target name", "self timer"],
}

SPEED_UP = {
    "id": "speed_up",
    "name": "Speed Up",
    "statuses_list": [
        {"id": "spd_up", "value": 2, "timer": 3,},
    ],
    "timer": 3, #only for commands with statuses_list
    "description": "Owner gets a bonus for its speed by 1 for 2 turns",
    "category": "Minor Buff",
    # if is_raw is false it means the damage dealt will be "pure" (desregarding atk and def bonuses)
    "max_range": 2,
    "msg": "{} is moving like the wind for {} turns",
    "msg_function": get_attrs,
    "msg_args": ["target name", "self timer"],
}

REGEN = {
    "id": "regen",
    "name": "Regeneration",
    "timer": long_timer, #only for commands with statuses_list
    "value": base_heal//2, #only for commands that deal/heal <value> hp
    "description": "Owner starts to regenerate!",
    "category": "Healing",
    "statuses_list": [
        {"id": "regen", "value": base_heal//2, "timer": long_timer,},
    ],
    "max_range": 2,
    "msg": "{} starts regenning {} hp for {} turns",
    "msg_function": get_attrs,
    "msg_args": ["target name", "self value", "self timer"]
}

'''
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
"id": ,
attack
heal
vamp_bite

sun_charge
golden_egg
multiply

perfect_counter

true_slash
toxic_shot
rage
shield_bash

power_up
defense_up
speed_up
regen
'''
