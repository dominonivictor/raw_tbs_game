from components.statuses import get_new_status_by_id
import constants.status_cons as sts_cons
from components.commands import get_new_command_by_id

#FUCK THIS IS BAD, I need to instanciate every time i do this, or else i just get references and
#things will go very badly
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
    "name": "Zarabatana",
    "value": 5,
    "statuses": [],
    "commands": [
        get_new_command_by_id("paralize_shot")
    ],
    "category": "ranged",
}

DAGGER = {
    "name": "Dagger",
    "value": 10,
    "statuses": [],
    "commands": [
        get_new_command_by_id("true_slash")
    ],
    "category": "meelee",

}

CAULDRON = {
    "name": "Cauldron",
    "value": 3,
    "statuses": [],
    "commands": [
        get_new_command_by_id("rage")
    ],
    "category": "meelee",
}

SHIELD = {
    "name": "Shield",
    "value": 3,
    "statuses": [
        get_new_status_by_id("def_up")
    ],
    "commands": [ 
        get_new_command_by_id("shield_bash")
    ],
    "category": "meelee",
}