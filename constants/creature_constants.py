
base_hp = 100
base_atk = 3
base_def = 1
base_spd = 4

hp_plus = 0
hp_minus = 0
atk_plus = 2
atk_minus = -1
def_plus = 1
def_minus = -1
spd_plus = 2
spd_minus = -1

creature_stats = {
    "fox":{
        "name": "Foxius",
        "hp": base_hp + hp_minus,
        "atk": base_atk + atk_plus,
        "def": base_def,
        "spd": base_spd,
        "race": "mamalia",
        "commands":[
            "attack",
            "vamp_bite",
            "toxic_shot",
            "power_up",
        ]
    },
    "turtle":{
        "name": "Turtlus",
        "hp": base_hp + hp_plus,
        "atk": base_atk + atk_minus,
        "def": base_def + def_plus,
        "spd": base_spd + spd_minus,
        "race": "reptalia",
        "commands":[
            "attack",
            "sun_charge",
            "power_up",
            "regen",
        ]
    },
    "chicken":{
        "name": "Chickenus",
        "hp": base_hp + hp_minus,
        "atk": base_atk + atk_plus,
        "def": base_def + def_minus,
        "spd": base_spd + spd_plus,
        "race": "aves",
        "commands":[
            "attack",
            "vamp_bite",
            "toxic_shot",
            "power_up",
        ]
    }
}

'''
<animal here>"":{
        "name": "",
        "hp": ,
        "atk": ,
        "def": ,
        "spd": ,
        "race": "",
        "commands":[
            "vamp_bite",
            "toxic_shot",
            "power_up",
            "attack"
        ]
    },

'''