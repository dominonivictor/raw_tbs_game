import pytest
from factories.actor_factory import get_new_actor

@pytest.fixture
def actor():
    return get_new_actor(test=True)

def test_actors_commands_are_different(actor):
    #TODO test knows too much of actor internals
    other_actor = get_new_actor(test=True)

    assert actor.get_commands_list() is not other_actor.get_commands_list()
    
def test_command_without_status(actor):
    #TODO test knows too much of actor and command internals
    attacking_actor = get_new_actor(test=True)
    attack = attacking_actor.get_command_by_id("attack")

    attack.set_target(actor)
    hp_before = actor.get_hp()
    attack.execute()

    assert actor.get_hp() < hp_before

def test_actor_recieves_new_status(actor):
    #TODO test knows too much of actor and command internals
    power_up = actor.get_command_by_id("power_up")
    actor_atk_before = actor.atk_stat
    power_up.set_target(actor)  #this is done by the tile selection
    power_up_value = power_up.statuses.list[0].value
    power_up.execute()
    
    assert actor_atk_before == actor.atk_stat - power_up_value 

def test_actor_recieves_heal(actor):
    #TODO test knows too much of actor and command internals
    heal = actor.get_command_by_id("heal")
    hp_before = actor.get_hp()

    heal.set_target(actor)
    heal.execute()
    assert actor.get_hp() == hp_before

    dmg_taken = 10
    actor.take_damage(value=dmg_taken)
    heal.execute()
    assert actor.get_hp() == hp_before - dmg_taken + heal.value

def test_rage_soup_gives_proper_buffs(actor):
    #TODO test knows too much of actor and command internals
    atk_before = actor.get_atk()
    def_before = actor.get_def()
    rage_soup = actor.get_command_by_id("rage")
    rage_soup.set_target(actor)
    rage_soup.execute()

    assert actor.atk_stat > atk_before and actor.def_stat < def_before

def test_sun_charge_proper_buffs(actor):
    #TODO test knows too much of actor and command internals
    atk_before = actor.atk_stat
    def_before = actor.def_stat
    spd_before = actor.spd_stat
    sun_charge = actor.get_command_by_id("sun_charge")
    sun_charge.target = actor
    sun_charge.execute()

    assert actor.atk_stat > atk_before and actor.def_stat > def_before and actor.spd_stat > spd_before

def test_learn_job_command():
    #TODO test knows too much of actor and command internals
    from components.jobs_commands import gen_jobs_list
    actor = get_new_actor(test=True)
    job_command = gen_jobs_list()[0]
    job_command.target = actor
    job_command.execute()
    assert actor.job is job_command.job

def test_equip_equip_command():
    #TODO test knows too much of actor and command internals
    from components.equips_commands import gen_equips_list
    actor = get_new_actor(test=True)
    equip_command = gen_equips_list()[0]
    equip_command.target = actor
    equip_command.execute()

    assert actor.equip is equip_command.equip
