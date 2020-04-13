'''
{
    "name":,
    "base_name": ,
    "value":,
    "timer":,
    "status_dict":{
        "atk_stat":,
    },
    "categoty":,
}
'''
STUNNED = {
    "name": "Stunned",
    "base_name": "stunned",
    "timer": 2,
    "category": "Major Debuff"
}

PERFECT_COUNTER_STANCE = {
    "name": "Perfect Counter Stance",
    "base_name": "perfect_counter_stance",
    "timer": 2,
    "category": "Major Buff"
}

ATK_UP = {
    "name": "Attack Up",
    "base_name": "buff",
    "timer": 2,
    "status_dict":{
        "atk_stat": 2,
    },
    "category": "Minor Buff",
}

DEF_UP = {
    "name": "Defense Up",
    "base_name": "buff",
    "timer": 2,
    "status_dict":{
        "def_stat": 2,
    },
    "category": "Minor Buff",
}

SPD_UP = {
    "name": "Speed Up",
    "base_name": "buff",
    "timer": 2,
    "status_dict":{
        "spd_stat": 2,
    },
    "category": "Minor Buff",
}

MAX_HP_UP = {
    "name": "Max Hp Up",
    "base_name": "buff",
    "timer": 2,
    "status_dict":{
        "max_hp": 2,
    },
    "category": "Minor Buff",
}

INCOME_UP = {
    "name": "Income Up",
    "base_name": "buff",
    "timer": 2,
    "status_dict":{
        "income": 2,
    },
    "category": "Minor Buff",
}

ENRAGED = {
    "name": "Enraged",
    "base_name": "buff",
    "timer": 2,
    "status_dict":{
        "atk_stat": 3,
        "def_stat": -4,
    },
    "category": "Major Buff",
}


REGENERATING = {
    "name":"Regenerating",
    "base_name": "hot",
    "value": 2,
    "timer": 4,
    "category": "HoT",
}

POISONED = {
    "name": "Poisoned",
    "base_name": "dot",
    "value": 2,
    "timer": 4,
    "category": "DoT",
}

BURNED = {
    "name": "Burned",
    "base_name": "dot",
    "value": 4,
    "timer": 2,
    "category": "DoT",
}

