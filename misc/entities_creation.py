from components.actors import Actor, Stat
from components.jobs import Guardian, Thief, Merchant, Hunter, Cook
from components.weapons import Zarabatana, Dagger, Cauldron, Shield
import components.commands as comm
import menus
from constants.creature_constants import creature_stats


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

def create_actor(animal):
    #animal recieves the animal string ex: "f"

    animal = creature_stats[animal]
    name = animal["name"].capitalize()
    hp_stat = Stat(value=animal["hp"])
    def_stat = Stat(value=animal["def"])
    atk_stat = Stat(value=animal["atk"])
    spd_stat = Stat(value=animal["spd"])
    income_stat = Stat(value=animal["income"])
    commands = create_commands_list(animal["commands"])
    
    actor = Actor(name=name, hp=hp_stat, def_stat=def_stat, 
        atk_stat=atk_stat, spd_stat=spd_stat, income_stat=income_stat,
        commands=commands)

    return actor
