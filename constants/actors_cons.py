
base_hp = 25
base_ap = 1
base_at = 3
base_df = 1
base_sp = 4

hp_plus = 5
hp_minus = -3
atk_plus = 2
atk_minus = -1
def_plus = 2
def_minus = -1
spd_plus = 1
spd_minus = -1
'''
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
'''
actors_stats = {
    "f":{
        "id": "fox",
        "animal": "fox",
        "letter": "F",
        "name": "Rogue",
        "stats": {
            "max_hp": base_hp,
            "hp": base_hp,
            "max_ap": base_ap,
            "ap": base_ap,
            "at": base_at,
            "df": base_df,
            "sp": base_sp,
        },
        "kingdom": "mamalia",
        "commands_ids":[
            "attack",
            "vamp_bite",
            "speed_up",
        ]
    },
    "t":{
        "id": "turtle",
        "animal": "turtle",
        "letter": "T",
        "name": "Kami",
        "stats": {
            "max_hp": base_hp,
            "hp": base_hp,
            "max_ap": base_ap,
            "ap": base_ap,
            "at": base_at,
            "df": base_df,
            "sp": base_sp,
        },
        "kingdom": "reptalia",
        "commands_ids":[
            "waterball",
            "regen",
            "defense_up",
        ]
    },
    "c":{
        "id": "chicken",
        "animal": "chicken",
        "letter": "C",
        "name": "Bugh Cohk",
        "stats": {
            "max_hp": base_hp,
            "hp": base_hp,
            "max_ap": base_ap,
            "ap": base_ap,
            "at": base_at,
            "df": base_df,
            "sp": base_sp,
        },
        "kingdom": "aves",
        "commands_ids":[
            "attack",
            "rage",
            "speed_up",
        ]
    },
    "a":{
        "id": "alligator",
        "animal": "alligator",
        "letter": "A",
        "name": "Shrek",
        "stats": {
            "max_hp": base_hp,
            "hp": base_hp,
            "max_ap": base_ap,
            "ap": base_ap,
            "at": base_at,
            "df": base_df,
            "sp": base_sp,
        },
        "kingdom": "reptalia",
        "commands_ids":[
            "attack",
            "vamp_bite",
            "power_up",
        ]
    },
    "p":{
        "id": "platypus",
        "animal": "platypus",
        "letter": "P",
        "name": "Perry",
        "stats": {
            "max_hp": base_hp,
            "hp": base_hp,
            "max_ap": base_ap,
            "ap": base_ap,
            "at": base_at,
            "df": base_df,
            "sp": base_sp,
        },
        "kingdom": "mamalia",
        "commands_ids":[
            "attack",
            "toxic_shot",
            "power_up",
        ]
    },
    "o":{
        "id": "owl",
        "animal": "owl",
        "letter": "O",
        "name": "Owrly",
        "stats": {
            "max_hp": base_hp,
            "hp": base_hp,
            "max_ap": base_ap,
            "ap": base_ap,
            "at": base_at,
            "df": base_df,
            "sp": base_sp,
        },
        "kingdom": "aves",
        "commands_ids":[
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
        "stats": {
            "max_hp": base_hp,
            "hp": base_hp,
            "max_ap": base_ap,
            "ap": base_ap,
            "at": base_at,
            "df": base_df,
            "sp": base_sp,
        }
        "kingdom": "",
        "commands_ids":[
            "toxic_shot",
            "power_up",
            "attack"
        ]
    },

'''
