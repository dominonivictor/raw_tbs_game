'''
{
    "name":,
    "base_name": ,
    "value":,
    "timer":,
    "category":,
    "attr": ,#optional, if impacts an actor attr
}

ids:
"stunned",
"perfect_counter_stance",
"atk_up",
"def_up",
"spd_up",
"max_hp_up",
"income_up",
"regen",
"poisoned",
"burned",
'''
STUNNED = {
    "id": "stunned",
    "name": "Stunned",
    "base_name": "stunned",
    "timer": 2,
    "category": "Major Debuff",
    
}

PERFECT_COUNTER_STANCE = {
    "id": "perfect_counter_stance",
    "name": "Perfect Counter Stance",
    "base_name": "perfect_counter_stance",
    "timer": 2,
    "category": "Major Buff"
}

ATK_UP = {
    "id": "atk_up",
    "name": "Attack Up",
    "base_name": "buff",
    "timer": 2,
    "value": 2,
    "category": "Minor Buff",
    "attr": "atk_stat",
}

DEF_UP = {
    "id": "def_up",
    "name": "Defense Up",
    "base_name": "buff",
    "timer": 2,
    "value": 2,
    "category": "Minor Buff",
    "attr": "def_stat",
}

SPD_UP = {
    "id": "spd_up",
    "name": "Speed Up",
    "base_name": "buff",
    "timer": 2,
    "value": 2,
    "category": "Minor Buff",
    "attr": "spd_stat",
}

MAX_HP_UP = {
    "id": "max_hp_up",
    "name": "Max Hp Up",
    "base_name": "buff",
    "timer": 2,
    "value": 2,
    "category": "Minor Buff",
    "attr": "max_hp_stat",
}

INCOME_UP = {
    "id": "income_up",
    "name": "Income Up",
    "base_name": "buff",
    "timer": 2,
    "value": 2,
    "category": "Minor Buff",
    "attr": "income_stat",
}

REGENERATING = {
    "id": "regen",
    "name":"Regenerating",
    "base_name": "hot",
    "value": 2,
    "timer": 4,
    "category": "HoT",
}

POISONED = {
    "id": "poisoned",
    "name": "Poisoned",
    "base_name": "dot",
    "value": 2,
    "timer": 4,
    "category": "DoT",
}

BURNED = {
    "id": "burned",
    "name": "Burned",
    "base_name": "dot",
    "value": 3,
    "timer": 3,
    "category": "DoT",
}

