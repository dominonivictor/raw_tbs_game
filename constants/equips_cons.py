import components.statuses as sts
import components.commands as comm
import constants.commands_cons as comm_con
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
        comm.ToxicShot(**comm_con.ZARABA_SHOT)
    ],
    "category": "ranged",
}

DAGGER = {
    "name": "Dagger",
    "value": 10,
    "statuses": [],
    "commands": [comm.Attack(**comm_con.DAGGER_ATTACK)],
    "category": "meelee",

}

CAULDRON = {
    "name": "Cauldron",
    "value": 3,
    "statuses": [],
    "commands": [comm.Rage(**comm_con.RAGE_SOUP)],
    "category": "meelee",
}

SHIELD = {
    "name": "Shield",
    "value": 3,
    "statuses": [sts.DefUp()],
    "commands": [
        comm.PerfectCounter(), 
        comm.Attack(**comm_con.SHIELD_BASH_ATTACK)
    ],
    "category": "meelee",
}