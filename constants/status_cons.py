'''
{
    "name":,
    "base_name": ,
    "value":,
    "timer":,
    "statuses":[], #empty if self, which i believe is all cases... is it possible a multi status? yes
    #sun charge is an example... but there it is ok... he isn't exacly a status but a command with statuses...
    "categoty":,
}
'''
STUNNED = {
    "name": "Stunned",
    "base_name": "stunned",
    "timer": 2,
    "category": "Major Debuff",
    
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
    "value": 2,
    "category": "Minor Buff",
    "attr": "atk_stat",
}

DEF_UP = {
    "name": "Defense Up",
    "base_name": "buff",
    "timer": 2,
    "value": 2,
    "category": "Minor Buff",
    "attr": "def_stat",
}

SPD_UP = {
    "name": "Speed Up",
    "base_name": "buff",
    "timer": 2,
    "value": 2,
    "category": "Minor Buff",
    "attr": "spd_stat",
}

MAX_HP_UP = {
    "name": "Max Hp Up",
    "base_name": "buff",
    "timer": 2,
    "value": 2,
    "category": "Minor Buff",
    "attr": "max_hp_stat",
}

INCOME_UP = {
    "name": "Income Up",
    "base_name": "buff",
    "timer": 2,
    "value": 2,
    "category": "Minor Buff",
    "attr": "income_stat",
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
    "value": 3,
    "timer": 3,
    "category": "DoT",
}

