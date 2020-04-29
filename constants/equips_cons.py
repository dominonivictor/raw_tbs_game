'''
{
    "name": ,
    "value": ,
    "statuses": [],
    "commands": [],
    "category": ,
}
'''
ZARABA = {
    "id": "zarabatana",
    "name": "Zarabatana",
    "value": 5,
    "statuses": [],
    "commands_func_params": "toxic_shot",
    "category": "ranged",
}

DAGGER = {
    "id": "dagger",
    "name": "Dagger",
    "value": 10,
    "statuses": [],
    "commands_func_params": "true_slash",
    "category": "meelee",

}

CAULDRON = {
    "id": "cauldron",
    "name": "Cauldron",
    "value": 3,
    "statuses": [],
    "commands_func_params": "rage",
    "category": "meelee",
}

from components.statuses import get_new_status_by_id

SHIELD = {
    "id": "shield",
    "name": "Shield",
    "value": 3,
    "statuses": [
        get_new_status_by_id(id="def_up")
    ],
    "commands_func_params": "shield_bash",
    "category": "meelee",
}