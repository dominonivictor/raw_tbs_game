from components.actors import Actor, Stat
from components.jobs import Guardian, Thief, Merchant, Hunter, Cook
from components.equips import Zarabatana, Dagger, Cauldron, Shield
import components.commands as comm
import menus
from constants.creature_cons import creature_stats
import constants.commands_cons as comm_cons


def create_commands_list(commands):
    #not very scalable... needs improving
    commands_list = []
    comm_dict = {
        'sun_charge': comm.SunCharge(**comm_cons.SUN_CHARGE),
        'toxic_shot': comm.ToxicShot(**comm_cons.TOXIC_SHOT),
        'attack': comm.Attack(**comm_cons.ATTACK),
        'heal': comm.Heal(**comm_cons.HEAL),
        'vamp_bite': comm.VampBite(**comm_cons.VAMP_BITE),
        'power_up': comm.PowerUp(**comm_cons.POWER_UP),
        'regen': comm.Regen(**comm_cons.REGEN),
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
