"""
{
    "name": ,
    "value": ,
    "statuses_list": [],
    "commands_ids": [],
    "category": ,
}
"""
ZARABA = {
    "id": "zarabatana",
    "name": "Zarabatana",
    "value": 5,
    "statuses_list": [],
    "commands_ids": ["toxic_shot"],
    "category": "ranged",
}

DAGGER = {
    "id": "dagger",
    "name": "Dagger",
    "value": 10,
    "statuses_list": [],
    "commands_ids": ["true_slash"],
    "category": "meelee",
}

CAULDRON = {
    "id": "cauldron",
    "name": "Cauldron",
    "value": 3,
    "statuses_list": [],
    "commands_ids": ["rage"],
    "category": "meelee",
}

SHIELD = {
    "id": "shield",
    "name": "Shield",
    "value": 3,
    "statuses_list": [{"id": "def_up", "value": 2, "timer": -1},],
    "commands_ids": ["shield_bash"],
    "category": "meelee",
}
