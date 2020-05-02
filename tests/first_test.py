import pytest
from components.actors import Actor

def test_actors_commands_are_different():
    a1 = Actor()
    a2 = Actor()

    assert a1.commands.list is not a2.commands.list
    
def test_actor_attacks_lose_proper_health():
    attacked_actor = Actor()
    attacking_actor = Actor(command_ids=["attack"])
    attack = attacking_actor.commands.list[0]
    attack.target = attacked_actor

    hp_before = attacked_actor.hp_stat

    attack.execute()

    assert attacked_actor.hp_stat == hp_before - (attack.value + attacking_actor.atk_stat -
            attacked_actor.def_stat)
