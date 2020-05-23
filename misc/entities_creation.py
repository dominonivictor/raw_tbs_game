from components.actors import Actor
from components.jobs import Guardian, Thief, Merchant, Hunter, Cook
from components.equips import get_new_equip_by_id
from components.commands import get_new_command_by_id
from constants.creature_cons import creature_stats

def create_commands_list(commands):
    #not very scalable... needs improving
    commands_list = []
    for command in commands:
        comm = get_new_command_by_id(id=command)
        commands_list.append(comm)

    return commands_list

def create_actor(animal, game):
    #animal recieves the animal string ex: "f"

    animal = creature_stats[animal]
    actor_dict = {
        "name": animal["name"],
        "animal": animal["animal"],
        "letter": animal["letter"],
        "kingdom": animal["kingdom"],
        "hp_stat": animal["hp_stat"],
        "def_stat": animal["def"],
        "atk_stat": animal["atk"],
        "spd_stat": animal["spd"],
        "income_stat": animal["income"],
        "commands_ids":animal["commands_ids"],

        "game_eye": game,
    }
    actor = Actor(**actor_dict)

    return actor
