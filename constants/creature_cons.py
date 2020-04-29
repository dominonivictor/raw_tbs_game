
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

creature_stats = {
    "f":{
        "animal": "fox",
        "letter": "F",
        "name": "Rogue",
        "hp": base_hp + hp_minus,
        "atk": base_atk + atk_plus,
        "def": base_def,
        "spd": base_spd,
        "income": base_income,
        "kingdom": "mamalia",
        "commands":[
            "attack",
            "vamp_bite",
            "speed_up",
        ]
    },
    "t":{
        "animal": "turtle",
        "letter": "T",
        "name": "Kami",
        "hp": base_hp + hp_plus,
        "atk": base_atk + atk_minus,
        "def": base_def + def_plus,
        "spd": base_spd + spd_minus,
        "income": base_income,
        "kingdom": "reptalia",
        "commands":[
            "attack",
            "regen",
            "defense_up",
        ]
    },
    "c":{
        "animal": "chicken",
        "letter": "C",
        "name": "Bugh Cohk",
        "hp": base_hp + hp_minus,
        "atk": base_atk + atk_plus,
        "def": base_def + def_minus,
        "spd": base_spd + spd_plus,
        "income": base_income,
        "kingdom": "aves",
        "commands":[
            "attack",
            "rage",
            "speed_up",
        ]
    },
    "a":{
        "animal": "alligator",
        "letter": "A",
        "name": "Shrek",
        "hp": base_hp,
        "atk": base_atk + atk_plus,
        "def": base_def,
        "spd": base_spd + spd_minus,
        "income": base_income,
        "kingdom": "reptalia",
        "commands":[
            "attack",
            "vamp_bite",
            "power_up",
        ]
    },
    "p":{
        "animal": "platypus",
        "letter": "P",
        "name": "Perry",
        "hp": base_hp + hp_minus,
        "atk": base_atk + atk_plus,
        "def": base_def + def_plus,
        "spd": base_spd + spd_minus,
        "income": base_income,
        "kingdom": "mamalia",
        "commands":[
            "attack",
            "toxic_shot",
            "power_up",
        ]
    },
    "o":{
        "animal": "owl",
        "letter": "O",
        "name": "Owrly",
        "hp": base_hp,
        "atk": base_atk + atk_plus,
        "def": base_def + def_minus,
        "spd": base_spd,
        "income": base_income,
        "kingdom": "aves",
        "commands":[
            "attack",
            "heal",
            "power_up",
        ]
    },
}

'''
    "":{
        "animal": ,
        "letter": ,
        "name": "",
        "hp": ,
        "atk": ,
        "def": ,
        "spd": ,
        "kingdom": "",
        "commands":[
            "vamp_bite",
            "toxic_shot",
            "power_up",
            "attack"
        ]
    },

'''