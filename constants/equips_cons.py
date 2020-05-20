'''
{
    "name": ,
    "value": ,
    "statuses_list": [],
    "commands": [],
    "category": ,
}
'''
ZARABA = {
    "id": "zarabatana",
    "name": "Zarabatana",
    "value": 5,
    "statuses_list": [],
    "commands_func_params": "toxic_shot",
    "category": "ranged",
}

DAGGER = {
    "id": "dagger",
    "name": "Dagger",
    "value": 10,
    "statuses_list": [],
    "commands_func_params": "true_slash",
    "category": "meelee",

}

CAULDRON = {
    "id": "cauldron",
    "name": "Cauldron",
    "value": 3,
    "statuses_list": [],
    "commands_func_params": "rage",
    "category": "meelee",
}

SHIELD = {
    "id": "shield",
    "name": "Shield",
    "value": 3,
    "statuses_list": [
        {"id": "def_up", "value": 2, "timer": -1},
    ],
    "commands_func_params": "shield_bash",
    "category": "meelee",
}
