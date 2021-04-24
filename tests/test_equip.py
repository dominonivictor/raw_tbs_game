import pytest
from factories.actor_factory import get_new_actor
from factories.equip_factory import get_new_equip
import constants.equips_cons as cons

@pytest.fixture
def actor():
    return get_new_actor(test=True)

def test_zarabatana():
    equip = get_new_equip(**cons.ZARABA)
    actor = get_new_actor(equip=equip)

    assert actor.has_command(cons.ZARABA["commands_ids"][0])
