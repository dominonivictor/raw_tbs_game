from components.actors import Actor, Stat
from components.jobs import Guardian, Thief
import components.commands as comm
from constants.creature_constants import creature_stats
from components.elements import Fire

def create_commands_list(commands):
    #not very scalable... needs improving
    commands_list = []
    comm_dict = {
        'sun_charge': comm.SunCharge(),
        'toxic_shot': comm.ToxicShot(),
        'attack': comm.Attack(),
        'heal': comm.Heal(),
        'vamp_bite': comm.VampBite(),
        'power_up': comm.PowerUp(),
        'regen': comm.Regen(),
    }
    for command in commands:
        commands_list.append(comm_dict.get(command, comm.Command()))

    return commands_list

def create_job(job):
    job = {
        'guardian': Guardian(),
        'thief': Thief(),
    }.get(job)

    return job

def create_actor(animal, job, equip):
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
        job=job, equipment=equip)

    actor.equipment.add_element(element=Fire())
    return actor

def handle_character_choice(choice, equip_num, equipments):
    animal, job = choice

    equip = equipments[equip_num - 1]

    animal = {
        't': 'turtle',
        'f': 'fox',
        'c': 'chicken'
    }.get(animal, "turtle")
    
    job = {
        'g': 'guardian',
        't': 'thief'
    }.get(job, "guardian")

    return create_actor(animal, job, equip)

def handle_action(comm_num, owner, target_num, actors):
    # action shall come as a number indicating 
    comm_num -= 1
    target_num -= 1
    command = owner.commands.list[comm_num]
    command.target = actors[target_num]
    return command
    

commands_options = """ choose an action:
                - Attack (a)
                - Heal (h)
                - Toxic Shot (t)
                - Vamp Bite (v)
                - Power Up (p)
                - Regen (b)
                """