from components.actors import Actor, Stat
from components.jobs import Guardian, Thief, Merchant, Hunter, Cook
from components.equips import Zarabatana, Dagger, Cauldron, Shield
from components.commands import instaciate_commands_dict
from constants.creature_cons import creature_stats

def create_commands_list(commands):
    #not very scalable... needs improving
    commands_list = []
    comm_dict = instaciate_commands_dict()
    for command in commands:
        comm = comm_dict.get(command)
        commands_list.append(comm)

    return commands_list

def create_job(job):
    job = {
        'g': Guardian(),
        't': Thief(),
        'm': Merchant(),
        'h': Hunter(),
        'c': Cook()
    }.get(job)

    return job

def create_equip(equip):
    equip = {
        'z': Zarabatana(),
        'd': Dagger(),
        'c': Cauldron(),
        's': Shield(),
    }.get(equip)

    return equip

def create_actor(animal, game):
    #animal recieves the animal string ex: "f"

    animal = creature_stats[animal]
    actor_dict = {
        "name": animal["name"],
        "animal": animal["animal"],
        "letter": animal["letter"],
        "kingdom": animal["kingdom"],
        "hp": Stat(value=animal["hp"]),
        "def_stat": Stat(value=animal["def"]),
        "atk_stat": Stat(value=animal["atk"]),
        "spd_stat": Stat(value=animal["spd"]),
        "income_stat": Stat(value=animal["income"]),
        "commands": create_commands_list(animal["commands"]),

        "game_eye": game,
    }

    actor = Actor(**actor_dict)

    return actor
