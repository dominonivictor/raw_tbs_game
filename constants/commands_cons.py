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
    "name": "Sun Charge",
    "status_dict": {
        "atk_stat": base_buff + buff_minus,
        "def_stat": base_buff + buff_minus,
        "spd_stat": base_buff + buff_minus,
    },
    "timer": mid_timer,
    "description": "Sun Charge increases all stats by 1 for 1 turn.",
    "category": "Greater Buff",
    "max_range": 2,
    "msg": "{} increases atk, def, spd by 1 for 2 turns",
    "msg_function": get_attrs,
    "msg_args": ["owner name"],
}

GOLDEN_EGG = {
    "name": "Golden Egg",
    "timer": 2, #only for commands with statuses
    "description": "Grants 2 random bonuses for 1 turn",
    "category": "Greater Buff",
    "status_dict": { #optional if command has stat buffs
        "atk_stat": 2,
        "def_stat": 2,
        "spd_stat": 2,
        "income_stat": 2,
    },
    "max_range": 1,
    "msg": "{} gets buffed on {} by 2? for 1 turn",
    "msg_function": get_attrs,
    "msg_args": ["owner name", "self choices"],
}

MULTIPLY = {
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

SHIELD_BASH_ATTACK = {
    "name": "Shield Bash",
    "value": 3, #only for commands that deal/heal <value> hp
    "description": "Bashes oponnent, leaving him stunned",
    "category": "Basic Attack",
    "status_dict": {
        "stunned": 2
    },
    "is_raw": False,
    "max_range": 1,
    "msg": "{} hits and stuns {} for {} damage",
    "msg_function": get_attrs,
    "msg_args": ["owner name", "target name", "self final_value"],
}

RAGE = {
    "name": "Rage",
    "timer": 2, #only for commands with statuses
    "description": "Someone is mad",
    "category": "Major Buff",
    "status_dict": { #optional if command has stat buffs
        "atk_stat": 3,
        "def_stat": -4,
    },
    "max_range": 3,
    "msg": "{} is enraged! (+ATK, -DEF)",
    "msg_function": get_attrs,
    "msg_args": ["owner name"],
}

RAGE_SOUP = {
    **RAGE,
    'name': 'Rage Soup'
}

PERFECT_COUNTER = {
    "name": "Perfect Counter",
    "timer": 2, #only for commands with statuses
    "description": "Full Counter",
    "category": "Major Buff",
    "status_dict": { #optional if command has stat buffs
        "perfect_counter_stance": 2
    },
    "max_range": 0,
    "msg": "{} takes a defensive stance",
    "msg_function": get_attrs,
    "msg_args": ["owner name"],
}

TOXIC_SHOT = {
    "name": "Toxic Shot",
    "status_dict":{
        "poisoned": 2
    },
    # "command_dict": {
    #     "attack": 2,
    # },
    "timer": mid_timer,
    "value": 2,
    "description": "Shoots target and poisons for 3 turns",
    "category": "Attack and DoT",
    "max_range": 3,
    "msg": "{} shots {} for {} damage and {} is posioned for {} turns",
    "msg_function": get_attrs,
    "msg_args": ["owner name", "target name", "self final_value", "target name", "self timer"],
}

#toxic and zaraba should be the same, probably remove this or rework it
ZARABA_SHOT = {
    "name": "Paralisis Shot",
    "status_dict":{
        "stunned": short_timer
    },
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
    "msg_args": ["owner name", "target name", "self final_value", "target name"],
}

POWER_UP = {
    "name": "Power Up",
    "status_dict": { #optional if command has stat buffs
        "atk_stat": base_buff,
    },
    "timer": 2, #only for commands with statuses
    "description": "Owner gets a bonus for its attack for 2 for 1 turn",
    "category": "Minor Buff",
    # if is_raw is false it means the damage dealt will be "pure" (desregarding atk and def bonuses)
    "max_range": 2,
    "msg": "{} gets powered up for {} turns",
    "msg_function": get_attrs,
    "msg_args": ["target name", "self timer"],
}

DEFENSE_UP = {
    "name": "Defense Up",
    "status_dict": { #optional if command has stat buffs
        "def_stat": base_buff,
    },
    "timer": 2, #only for commands with statuses
    "description": "Owner gets a bonus for its defense for 2 for 1 turn",
    "category": "Minor Buff",
    # if is_raw is false it means the damage dealt will be "pure" (desregarding atk and def bonuses)
    "max_range": 2,
    "msg": "{} strenghtens defenses for {} turns",
    "msg_function": get_attrs,
    "msg_args": ["target name", "self timer"],
}

SPEED_UP = {
    "name": "Speed Up",
    "status_dict": { #optional if command has stat buffs
        "spd_stat": base_buff + buff_minus,
    },
    "timer": 3, #only for commands with statuses
    "description": "Owner gets a bonus for its speed by 1 for 2 turns",
    "category": "Minor Buff",
    # if is_raw is false it means the damage dealt will be "pure" (desregarding atk and def bonuses)
    "max_range": 2,
    "msg": "{} is moving like the wind for {} turns",
    "msg_function": get_attrs,
    "msg_args": ["target name", "self timer"],
}

REGEN = {
    "name": "Regeneration",
    "timer": long_timer, #only for commands with statuses
    "value": base_heal//2, #only for commands that deal/heal <value> hp
    "description": "Owner starts to regenerate!",
    "category": "Healing",
    "status_dict":{
        "regen": base_heal//2
    },
    "max_range": 2,
    "msg": "{} starts regenning 2 hp for 4 turns",
    "msg_function": get_attrs,
    "msg_args": ["target name"]
}

'''
{
    "name": ,
    "timer": , #only for commands with statuses
    "value": , #only for commands that deal/heal <value> hp
    "description": ,
    "category": ,
    "eff" : , #for now only for VampBite(), it shows the efficiency of the vampire bite heal
    "is_raw": , # default is False, only valid for commands that use Attack()
    # if is_raw is false it means the damage dealt will be "pure" (desregarding atk and def bonuses)
    "status_dict": { #optional if command has stat buffs
        <status_name>: status_value
    },
    "command_dict": {
        <command_name>: command_value
    },
    "max_range": 1,
}
'''