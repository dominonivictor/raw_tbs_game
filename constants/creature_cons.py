base_hp = 25
base_atk = 3
base_def = 1
base_spd = 4
base_income = 1

hp_plus = 5
hp_minus = -3
atk_plus = 2
atk_minus = -1
def_plus = 2
def_minus = -1
spd_plus = 1
spd_minus = -1

"""
commands_ids:

    "attack",
    "heal",
    "power_up",
    "rage",
    "speed_up",
    "regen",
    "toxic_shot",
    "defense_up",
    "vamp_bite",
    "speed_up",
"""

creature_stats = {
    "f": {
        "animal": "fox",
        "letter": "F",
        "name": "Rogue",
        "hp_stat": base_hp + hp_minus,
        "atk": base_atk + atk_plus,
        "def": base_def,
        "spd": base_spd,
        "income": base_income,
        "kingdom": "mamalia",
        "commands_ids": ["attack", "vamp_bite", "speed_up",],
    },
    "t": {
        "animal": "turtle",
        "letter": "T",
        "name": "Kami",
        "hp_stat": base_hp + hp_plus,
        "atk": base_atk + atk_minus,
        "def": base_def + def_plus,
        "spd": base_spd + spd_minus,
        "income": base_income,
        "kingdom": "reptalia",
        "commands_ids": ["waterball", "regen", "defense_up",],
    },
    "c": {
        "animal": "chicken",
        "letter": "C",
        "name": "Bugh Cohk",
        "hp_stat": base_hp + hp_minus,
        "atk": base_atk + atk_plus,
        "def": base_def + def_minus,
        "spd": base_spd + spd_plus,
        "income": base_income,
        "kingdom": "aves",
        "commands_ids": ["attack", "rage", "speed_up",],
    },
    "a": {
        "animal": "alligator",
        "letter": "A",
        "name": "Shrek",
        "hp_stat": base_hp,
        "atk": base_atk + atk_plus,
        "def": base_def,
        "spd": base_spd + spd_minus,
        "income": base_income,
        "kingdom": "reptalia",
        "commands_ids": ["attack", "vamp_bite", "power_up",],
    },
    "p": {
        "animal": "platypus",
        "letter": "P",
        "name": "Perry",
        "hp_stat": base_hp + hp_minus,
        "atk": base_atk + atk_plus,
        "def": base_def + def_plus,
        "spd": base_spd + spd_minus,
        "income": base_income,
        "kingdom": "mamalia",
        "commands_ids": ["poison_tail", "toxic_shot", "power_up",],
    },
    "o": {
        "animal": "owl",
        "letter": "O",
        "name": "Owrly",
        "hp_stat": base_hp,
        "atk": base_atk + atk_plus,
        "def": base_def + def_minus,
        "spd": base_spd,
        "income": base_income,
        "kingdom": "aves",
        "commands_ids": ["wind_blow", "heal", "power_up",],
    },
}

"""
    "":{
        "animal": ,
        "letter": ,
        "name": "",
        "hp_stat": ,
        "atk": ,
        "def": ,
        "spd": ,
        "kingdom": "",
        "commands_ids":[
            "toxic_shot",
            "power_up",
            "attack"
        ]
    },

"""
