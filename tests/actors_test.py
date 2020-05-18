import pytest
from factories.actor_factory import get_new_actor


def test_actors_commands_are_different():
    a1 = get_new_actor(test=True)
    a2 = get_new_actor(test=True)

    assert a1.commands.list is not a2.commands.list
    
def test_actor_attacks_lose_proper_health():
    attacked_actor = get_new_actor(test=True)
    attacking_actor = get_new_actor(test=True)
    attack = attacking_actor.commands.get_command_by_id("attack")

    attack.target = attacked_actor

    hp_before = attacked_actor.hp_stat

    attack.execute()
    assert attacked_actor.hp_stat == hp_before - (attack.value + attacking_actor.atk_stat -
            attacked_actor.def_stat)

def test_actor_recieves_new_status():
    actor = get_new_actor(test=True)
    power_up = actor.commands.get_command_by_id("power_up")
    actor_atk_before = actor.atk_stat
    power_up.target = actor #this is done by the tile selection
    power_up_value = power_up.statuses.list[0].value
    power_up.execute()
    
    assert actor_atk_before == actor.atk_stat - power_up_value 

def test_actor_recieves_heal():
    actor = get_new_actor(test=True)
    heal = actor.commands.get_command_by_id("heal")
    hp_before = actor.hp_stat

    heal.target = actor
    heal.execute()
    assert actor.hp_stat == hp_before

    dmg_taken = 10
    actor.take_damage(value=dmg_taken)
    heal.execute()
    assert actor.hp_stat == hp_before - dmg_taken + heal.value

def test_rage_soup_gives_proper_buffs():
    actor = get_new_actor(test=True)
    atk_before = actor.atk_stat
    def_before = actor.def_stat
    rage_soup = actor.commands.get_command_by_id("rage")
    rage_soup.target = actor
    rage_soup.execute()

    assert actor.atk_stat > atk_before and actor.def_stat < def_before

def test_sun_charge_proper_buffs():
    actor = get_new_actor(test=True)
    atk_before = actor.atk_stat
    def_before = actor.def_stat
    spd_before = actor.spd_stat
    sun_charge = actor.commands.get_command_by_id("sun_charge")
    sun_charge.target = actor
    sun_charge.execute()

    assert actor.atk_stat > atk_before and actor.def_stat > def_before and actor.spd_stat > spd_before

def test_learn_job_command():
    from components.jobs_commands import gen_jobs_list
    actor = get_new_actor(test=True)
    job_command = gen_jobs_list()[0]
    job_command.target = actor
    job_command.execute()
    assert actor.job is job_command.job

def test_equip_equip_command():
    from components.equips_commands import gen_equips_list
    actor = get_new_actor(test=True)
    equip_command = gen_equips_list()[0]
    equip_command.target = actor
    equip_command.execute()

    assert actor.equip is equip_command.equip
