default = None
base_atk = 3
base_heal = 4
base_buff = 2
vamp_bite_eff = 0.5
short_timer = 5 # 1 round
mid_timer = 3 # 2 rounds
long_timer = 4 # 3 rounds

ATTACK = {
    "name": "Punch",
    "value": base_atk, #only for commands that deal/heal <value> hp
    "description": "Gives a good old punch to the face",
    "category": "Basic Attack",  
    "is_raw": False,
    "max_range": 1,  
}

HEAL = {
    "name": "Healing Salve",
    "value": base_heal, #only for commands that deal/heal <value> hp
    "description": "Gives a healing salve to the target",
    "category": "Basic Heal",  
    "max_range": 2, 
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
}

SUN_CHARGE = {
    "name": "Sun Charge",
    "status_dict": {
        "atk_stat": base_buff,
        "def_stat": base_buff,
        "spd_stat": base_buff
    },
    "timer": short_timer,
    "description": "Sun Charge increases all stats by 2 for 1 turn.",
    "category": "Greater Buff",
    "max_range": 2,
}

TOXIC_SHOT = {
    "name": "Toxic Shot",
    "status_dict":{
        "poisoned": 2
    },
    "command_dict": {
        "attack": 2,
    },
    "timer": mid_timer,
    "value": 2,
    "description": "Shoots target and poisons for 3 turns",
    "category": "Attack and DoT",
    "max_range": 3,
}

POWER_UP = {
    "name": "Power Up",
    "status_dict": { #optional if command has stat buffs
        "atk_stat": base_buff,
    },
    "timer": 2, #only for commands with statuses
    "description": "Owner gets a bonus for its attack for 2",
    "category": "Minor Buff",
    # if is_raw is false it means the damage dealt will be "pure" (desregarding atk and def bonuses)
    "max_range": 2,
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
}

SHIELD_BASH = {
    "name": "Shield Bash",
    "value": 5, #only for commands that deal/heal <value> hp
    "description": "Bashy bash",
    "category": "Utility Attack",
    "is_raw": False, # default is False, only valid for commands that use Attack()
    # if is_raw is True it means the damage dealt will be "pure" (desregarding atk and def bonuses)
    "status_dict": { #optional if command has stat buffs
        "stunned": 2
    },
    "command_dict": {
        "attack": 5
    },
    "max_range": 1,
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