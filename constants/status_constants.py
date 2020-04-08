'''
{
    "name":,
    "value":,
    "timer":,
    "status_dict":{
        "atk_stat":,
    },
    "categoty":,
}
'''

ATK_UP = {
    "name": "Attack Up",
    "timer": 2,
    "status_dict":{
        "atk_stat": 2,
    },
    "category": "Minor Buff",
}

DEF_UP = {
    "name": "Defense Up",
    "timer": 2,
    "status_dict":{
        "def_stat": 2,
    },
    "category": "Minor Buff",
}

SPD_UP = {
    "name": "Speed Up",
    "timer": 2,
    "status_dict":{
        "spd_stat": 2,
    },
    "category": "Minor Buff",
}


REGENERATING = {
    "name":"Regenerating",
    "value": 2,
    "timer": 4,
    "category": "HoT",
}

POISONED = {
    "name": "Poisoned",
    "value": 2,
    "timer": 3,
    "category": "DoT",
}

BURNED = {
    "name": "Burned",
    "value": 25,
    "timer": 4,
    "category": "DoT",
}