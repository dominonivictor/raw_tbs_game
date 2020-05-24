import pytest
from factories.actor_factory import get_new_actor 

@pytest.fixture
def actor():
    return get_new_actor(test=True)

def test_actors_commands_are_different(actor):
    other_actor = get_new_actor(test=True)

    assert actor.list_commands() is not other_actor.list_commands()
    
def test_actor_show_battle_stats(actor):
    from factories.equip_factory import get_new_equip
    equip = get_new_equip()
    
    actor.add_equip(equip)
    try:
        actor.show_battle_stats()
    except:
        assert "ERROR SHOW BATTLE STATS IS FAULTY" == 0

