from components.actors import Actor, Stat
from components.jobs import Guardian, Thief
import components.commands as comm
from constants.creature_constants import creature_stats

def create_commands_list(commands):
    #not very scalable... needs improving
    commands_list = []
    for command in commands:
        if command == 'sun_charge': commands_list.append(comm.SunCharge())
        elif command == 'toxic_shot': commands_list.append(comm.ToxicShot())
        elif command == 'attack': commands_list.append(comm.Attack())
        elif command == 'heal': commands_list.append(comm.Heal())
        elif command == 'vamp_bite': commands_list.append(comm.VampBite())
        elif command == 'power_up': commands_list.append(comm.PowerUp())
        elif command == 'regen': commands_list.append(comm.Regen())

    return commands_list

def create_job(job):
    if job is 'guardian':
        job = Guardian()
    elif job is 'thief':
        job = Thief()

    return job

def create_actor(animal, job):
    animal = creature_stats[animal]
    name = animal["name"].capitalize()
    hp_stat = Stat(value=animal["hp"])
    def_stat = Stat(value=animal["def"])
    atk_stat = Stat(value=animal["atk"])
    spd_stat = Stat(value=animal["spd"])
    commands = create_commands_list(animal["commands"])
    job = create_job(job)
    actor = Actor(name=name, hp=hp_stat, def_stat=def_stat, 
        atk_stat=atk_stat, spd_stat=spd_stat, commands=commands,
        job=job)

    return actor

def handle_character_choice(choice):
    animal = choice[0]
    job = choice[1]

    if animal is 't':
        animal = "turtle"

    elif animal is 'f':
        animal = "fox"

    elif animal is 'c':
        animal = "chicken"

    if job is 'g':
        job = "guardian"
    elif job is 't':
        job = "thief"
    else:
        job = None

    return create_actor(animal, job)

def handle_action(comm_num, owner, target_num, entities):
    # action shall come as a number indicating 
    comm_num -= 1
    target_num -= 1

    command = owner.commands.list[comm_num]
    command.target = entities[target_num]
    
    return command
    

commands_options = """ choose an action:
                - Attack (a)
                - Heal (h)
                - Toxic Shot (t)
                - Vamp Bite (v)
                - Power Up (p)
                - Regen (b)
                """