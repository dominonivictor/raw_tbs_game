import pytest
from raw_tbs_game.factories.actor_factory import get_new_actor
from raw_tbs_game.factories.equip_factory import get_new_equip
'''
### BASICS
attack OK
heal OK
vamp_bite OK

### KINGDOM
sun_charge OK
golden_egg
multiply

### JOBS
perfect_counter
copy_cat
mixn

### EQUIPS
true_slash
toxic_shot OK
shield_bash
rage_soup
paralize_shot

### STATUSES
power_up OK
defense_up
speed_up
regen

### LEARN/EQUIP
learn_job_command OK
equip_equip_command OK
'''

@pytest.fixture
def actor():
    return get_new_actor(test=True)

############# BASICS
def test_atk(actor):
    #TODO test knows too much of the names of ids
    attacking_actor = get_new_actor(test=True)
    attack = attacking_actor.get_command_by_id("attack")
    attack.set_target(actor)
    hp_before = actor.hp_stat
    attack.execute()

    assert actor.hp_stat < hp_before

def test_heal(actor):
    #TODO test knows too much of actor and command internals
    heal = actor.get_command_by_id("heal")
    hp_before = actor.hp_stat

    heal.set_target(actor)
    heal.execute()
    assert actor.hp_stat == hp_before

    dmg_taken = 10
    actor.take_damage(value=dmg_taken)
    heal.execute()
    assert actor.hp_stat == hp_before - dmg_taken + heal.value

def test_vamp_bite(actor):
    attacking_actor = get_new_actor(test=True)
    vamp_bite = attacking_actor.get_command_by_id("vamp_bite")
    attacking_actor.take_damage(5)

    vamp_bite.set_target(actor)
    victim_hp_before = actor.hp_stat
    attacker_hp_before = attacking_actor.hp_stat

    vamp_bite.execute()

    assert attacking_actor.hp_stat > attacker_hp_before
    assert actor.hp_stat < victim_hp_before

############# KINGDOM

def test_sun_charge(actor):
    #TODO test knows too much of actor and command internals
    atk_before = actor.atk_stat
    def_before = actor.def_stat
    spd_before = actor.stats.sp
    sun_charge = actor.get_command_by_id("sun_charge")
    sun_charge.set_target(actor)
    sun_charge.execute()

    assert actor.atk_stat > atk_before and actor.def_stat > def_before and actor.stats.sp > spd_before

def test_golden_egg(actor):
    golden_egg = actor.get_command_by_id("golden_egg")
    def get_stats_sum(actor):
        stats_sum = (actor.hp_stat + actor.atk_stat + actor.def_stat +
               actor.stats.sp + actor.income_stat)
        return stats_sum

    stats_before = get_stats_sum(actor)
    golden_egg.set_target(actor)
    golden_egg.execute()

    assert stats_before < get_stats_sum(actor)

'''
def multiply(actor):
    #How do I tackle this???
    #maybe just check the return?
    #i cant even execute... cause the board is not on...
    #I have to make the API clear what do commands do? how do i return this?
    #why
    multi = actor.get_command_by_id("multiply")

    pass
'''

############# JOBS
def test_perfect_counter(actor):
    perfect_counter = actor.get_command_by_id("perfect_counter")
    perfect_counter.set_target(actor)
    perfect_counter.execute()

    assert actor.has_status("perfect_counter_stance")

def test_copy_cat(actor):
    #still needs to test the forget method
    thief = get_new_actor(commands_ids=["copy_cat"])
    length_before = len(thief.list_commands())
    copy_cat = thief.get_command_by_id("copy_cat")
    copy_cat.set_target(actor)
    copy_cat.execute()

    assert len(thief.list_commands()) == length_before + 1
    copy_cat.execute()
    assert len(thief.list_commands()) == length_before

def test_mixn(actor):
    #this requires more setup... need to generate equip and to test equip maybe not
    #attacking with elemental equip is another thing...
    equip = get_new_equip()
    actor_with_equip = get_new_actor(equip=equip)
    mixn = actor.get_command_by_id("mixn")
    mixn.set_target(actor_with_equip)
    mixn.execute()

    assert equip.has_element()

############# EQUIPS
def test_true_slash(actor):
    true_slash = actor.get_command_by_id("true_slash")
    actor.set_def(1000)
    hp_before = actor.hp_stat
    true_slash.set_target(actor)
    true_slash.execute()

    assert hp_before > actor.hp_stat

def test_toxic_shot(actor):
    attacking_actor = get_new_actor(test=True)
    toxic_shot = attacking_actor.get_command_by_id("toxic_shot")
    toxic_shot.set_target(actor)
    #TODO this is messy, knows too much of internals
    hp_before = actor.hp_stat
    timer = toxic_shot.statuses.list[0].timer
    value = toxic_shot.statuses.list[0].value
    toxic_shot.execute()

    assert actor.has_status("poisoned")
    assert actor.get_status("poisoned")
    assert actor.hp_stat < hp_before

def test_shield_bash(actor):
    shield_bash = actor.get_command_by_id("shield_bash")
    hp_before = actor.hp_stat
    shield_bash.set_target(actor)
    shield_bash.execute()

    assert actor.has_status("stunned")
    assert hp_before > actor.hp_stat

def test_rage_soup(actor):
    atk_before = actor.atk_stat
    def_before = actor.def_stat
    rage_soup = actor.get_command_by_id("rage")
    rage_soup.set_target(actor)
    rage_soup.execute()

    assert actor.atk_stat > atk_before and actor.def_stat < def_before

def test_paralize_shot(actor):
    para_shot = actor.get_command_by_id("paralize_shot")
    hp_before = actor.hp_stat
    para_shot.set_target(actor)
    para_shot.execute()


############# STATUSES
'''There is a slight problem here that these commands are kinda testing the
command but are also testing the status behavior... these should be separated!
'''
def test_power_up(actor):
    #TODO test knows too much of statuses internals
    power_up = actor.get_command_by_id("power_up")
    actor_atk_before = actor.atk_stat
    power_up.set_target(actor)  #this is done by the tile selection
    value = power_up.get_statuses_values(pos=0)
    timer = power_up.get_timer()
    power_up.execute()

    assert actor_atk_before == actor.atk_stat - value
    for _ in range(timer):
        actor.pass_time()
    assert actor_atk_before == actor.atk_stat

def test_defense_up(actor):
    defense_up = actor.get_command_by_id("defense_up")
    actor_def_before = actor.def_stat
    defense_up.set_target(actor)  #this is done by the tile selection
    value = defense_up.get_statuses_values(pos=0)
    timer = defense_up.get_timer()
    defense_up.execute()

    assert actor_def_before == actor.def_stat - value
    for _ in range(timer):
        actor.pass_time()
    assert actor_def_before == actor.def_stat

def test_speed_up(actor):
    speed_up = actor.get_command_by_id("speed_up")
    actor_spd_before = actor.stats.sp
    speed_up.set_target(actor)  #this is done by the tile selection
    value = speed_up.get_statuses_values(pos=0)
    timer = speed_up.get_timer()
    speed_up.execute()

    assert actor_spd_before == actor.stats.sp - value
    for _ in range(timer):
        actor.pass_time()
    assert actor_spd_before == actor.stats.sp

def test_regen(actor):
    regen = actor.get_command_by_id("regen")
    regen.set_target(actor)
    timer = regen.get_timer()
    actor.take_damage(20)
    regen.execute()
    assert actor.has_status("regen")
    for _ in range(timer):
        hp_before = actor.hp_stat
        actor.pass_time()
        assert hp_before < actor.hp_stat

    actor.pass_time()
    assert not actor.has_status("regen")

############# LEARN/EQUIP
def test_learn_job_command():
    #TODO test knows too much of actor and command internals
    actor = get_new_actor()
    actor2 = get_new_actor()

    from raw_tbs_game.components.jobs_commands import gen_jobs_list
    commands_length = len(actor.list_commands())
    status_length = len(actor.list_statuses())

    job_command = gen_jobs_list()[0]
    job_command2 = gen_jobs_list()[0]
    job_command.set_target(actor)
    job_command2.set_target(actor2)
    job_command.execute()
    job_command2.execute()
    #too many asserts!!!!!
    assert actor.job is job_command.job
    assert job_command.job.name == "Guardian"
    assert commands_length + 1 == len(actor.list_commands())
    assert commands_length + 1 == len(actor2.list_commands())
    assert status_length + 1 == len(actor.list_statuses()) == len(actor2.list_statuses())
    #test knows too much of actor internals
    assert actor.list_commands()[-1].id == actor2.list_commands()[-1].id

def test_equip_equip_command(actor):
    #TODO test is giving kind of a false positive, when clicking on the actor we get an error... 
    from raw_tbs_game.components.equips_commands import gen_equips_list
    equip_command = gen_equips_list()[0]
    equip_command.set_target(actor)
    equip_command.execute()

    assert actor.equip is equip_command.equip


############## AOE
def create_mock_game_board(grid_size):
    grid = [[Tile() for _ in range(grid_size)] for _ in range(grid_size)]
    return list(map(list, zip(*grid))) #doing this to transpose, is it needed though?

from map_objects.tile import Tile

class MockGame():
    def __init__(self):

        grid = [[Tile() for _ in range(3)] for _ in range(3)]
        self.grid = list(map(list, zip(*grid)))

    def set_actor_on_xy(self, actor, x, y):
        self.grid[x][y].actor = actor

    def has_actor_on_xy(self, x, y):
        return bool(self.grid[x][y].actor)

    def get_actor_on_xy(self, x, y):
        return self.grid[x][y].actor



def test_waterball(actor):
    waterball = actor.get_command_by_id("waterball")
    mock_game = MockGame()
    waterball.game_eye = mock_game

    target_in_range = get_new_actor()
    target_in_range.set_pos(x=1, y=1)
    in_range_hp_before = target_in_range.hp_stat

    target_out_of_range = get_new_actor()
    target_out_of_range.set_pos(x=0, y=0)
    out_range_hp_before = target_out_of_range.hp_stat

    mock_game.set_actor_on_xy(target_out_of_range, 0, 0)
    mock_game.set_actor_on_xy(target_in_range, 1, 1)
    #put actors on the board
    waterball.set_target_pos((1, 1))
    waterball.execute()

    assert target_in_range.hp_stat < in_range_hp_before
    assert target_out_of_range.hp_stat == out_range_hp_before



