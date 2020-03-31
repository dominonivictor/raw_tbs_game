from components import Actor, Stat
from commands import Attack, Heal
import game_states


class Game():
    def __init__(self):
        self.state = game_states.START
        self.log = []
        self.event_list = []
        self.p1 = None
        self.p2 = None

    def main_loop(self):
        if self.state == game_states.START:
            choice = input("""Welcome, choose p1 character:
                - Turtle (t)
                - Fox (f)
                - Chicken (c)\n\n""")
            self.p1 = handle_character_choice(choice)
            choice = input("""Welcome, choose p2 character:
                - Turtle (t)
                - Fox (f)
                - Chicken (c)\n""")
            self.p2 = handle_character_choice(choice)
            print(f"p1: {self.p1.name} VS p2: {self.p2.name}")
            self.state = game_states.BATTLE

        elif self.state is game_states.BATTLE:
            choice = input("""P1 choose an action:
                - Attack (a)
                - Heal (h)""")
            action = handle_action(choice, self.p1, self.p2)
            self.event_list.append(action)
            choice = input("""P2 choose an action:
                - Attack (a)
                - Heal (h)""")
            action = handle_action(choice, self.p2, self.p1)
            self.event_list.append(action)
            self.state = game_states.PAUSE

        elif self.state is game_states.PAUSE:
            print(f"p1 hp: {self.p1.hp.value} / p2 hp: {self.p2.hp.value}")
            self.state = game_states.BATTLE

        
        for event in self.event_list:
            msg = event.execute()
            print(f"{msg['msg']}")
        
        self.event_list = []


def handle_character_choice(choice):
    actor = ''
    if choice is 't':
        hp = Stat(value=12)
        def_stat = Stat(value=1)
        atk_stat = Stat(value=-1)
        actor = Actor(name="Turtle", hp=hp, def_stat=def_stat, atk_stat=atk_stat)
    elif choice is 'f':
        hp = Stat(value=10)
        def_stat = Stat(value=0)
        atk_stat = Stat(value=0)
        actor = Actor(name="Fox", hp=hp, def_stat=def_stat, atk_stat=atk_stat)
    elif choice is 'c':
        hp = Stat(value=8)
        def_stat = Stat(value=-1)
        atk_stat = Stat(value=1)
        actor = Actor(name="Chicken", hp=hp, def_stat=def_stat, atk_stat=atk_stat)

    return actor

def handle_action(choice, owner, target):
    action = ''
    if choice is 'a':
        action = Attack(owner, target, 3)
    elif choice is 'h':
        action = Heal(owner, owner, 2)

    return action
    
    

if __name__ == '__main__':
    game = Game()
    while True:
        game.main_loop()