import components.statuses as sts
import components.commands as comm
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
    "commands": [comm.ToxicShot(name="Zulu Toxin Shot", value=5, status_dict={"poisoned": 4})],
    "category": "ranged",
}

DAGGER = {
    "name": "Dagger",
    "value": 10,
    "statuses": [],
    "commands": [comm.Attack(name="Slash", value=10, is_raw=True)],
    "category": "meelee",

}

CAULDRON = {
    "name": "Cauldron",
    "value": 3,
    "statuses": [],
    "commands": [comm.Rage(name="Rage Soup")],
    "category": "meelee",
}

SHIELD = {
    "name": "Shield",
    "value": 3,
    "statuses": [sts.DefUp()],
    "commands": [
        comm.PerfectCounter(), 
        comm.Attack(name="Shield Bash", value=3, status_dict={"stun": 2})],
    "category": "meelee",
}