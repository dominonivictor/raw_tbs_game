from components.actors import Actor
from components.jobs import Guardian, Thief, Merchant, Hunter, Cook
from components.equips import get_new_equip_by_id
from components.commands import get_new_command_by_id
from constants.actors_cons import actors_stats

def create_commands_list(commands):
    #not very scalable... needs improving
    commands_list = []
    for command in commands:
        comm = get_new_command_by_id(id=command)
        commands_list.append(comm)

    return commands_list

def create_actor(animal, game):
    #animal recieves the animal string ex: "f"

    animal = actors_stats[animal]
    actor_dict = {
        **animal,
        "game_eye": game,
    }
    actor = Actor(**actor_dict)

    return actor
