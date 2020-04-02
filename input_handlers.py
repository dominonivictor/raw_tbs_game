from components import Actor, Stat
from commands import SunCharge
from creature_constants import creature_stats

def handle_character_choice(choice):
    actor = ''
    if choice is 't':
        hp = Stat(value=12)
        def_stat = Stat(value=1)
        atk_stat = Stat(value=-1)
        actor = Actor(name="Turtle", hp=hp, def_stat=def_stat, atk_stat=atk_stat)

    elif choice is 'f':
        fox = creature_stats["fox"]
        hp_stat = Stat(value=fox["hp"])
        def_stat = Stat(value=fox["def"])
        atk_stat = Stat(value=fox["atk"])
        race_skill = SunCharge()
        actor = Actor(name="Fox", hp=hp_stat, def_stat=def_stat, atk_stat=atk_stat, skills=[race_skill])

    elif choice is 'c':
        hp = Stat(value=8)
        def_stat = Stat(value=-1)
        atk_stat = Stat(value=1)
        actor = Actor(name="Chicken", hp=hp, def_stat=def_stat, atk_stat=atk_stat)

    return actor

def handle_action(choice, owner, target):
    action = ''
    if choice is 'a':
        action = Attack(owner=owner, target=target, value=3)
    elif choice is 'h':
        action = Heal(owner=owner, target=owner, value=2)
    elif choice is 't':
        action = ToxicShot(value=1, timer=3, target=target)
    elif choice is 'v':
        action = VampBite(owner=owner, target=target)
    elif choice is 'p':
        action = PowerUp(owner=owner, target=owner)
    elif choice is 'b':
        action = Blessing(owner=owner, target=owner)
    elif choice is 's':
        action = SunCharge(owner=owner, target=owner)

    return action
    

skills_options = """ choose an action:
                - Attack (a)
                - Heal (h)
                - Toxic Shot (t)
                - Vamp Bite (v)
                - Power Up (p)
                - Blessing (b)
                """