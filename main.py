from commands import Attack, Heal, VampBite, PowerUp, Blessing
import game_states

skills_options = """ choose an action:
                - Attack (a)
                - Heal (h)
                - Toxic Shot (t)
                - Vamp Bite (v)
                - Power Up (p)
                - Blessing (b)
                """

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
            print("++++++++++++++++ BATTLE ++++++++++++++++++++++")
            choice = input(f"""P1 {skills_options}""")
            action = handle_action(choice, self.p1, self.p2)
            self.event_list.append(action)
            choice = input(f"""P2 {skills_options}""")
            action = handle_action(choice, self.p2, self.p1)
            self.event_list.append(action)
            self.state = game_states.PAUSE
            print("++++++++++++++++++++++++++++++++++++++++++++++")

        elif self.state is game_states.PAUSE:
            print("========== IN BETWEEN TURNS ===============")
            name_list = [s.name for s in self.p1.statuses.list]
            name_list2 = [s.name for s in self.p2.statuses.list]
            timer_list = [s.timer for s in self.p1.statuses.list]
            timer_list2 = [s.timer for s in self.p2.statuses.list]
            print(f"STATUS: p1 {name_list} for  {timer_list}, p2 BATTLE  {name_list2} for {timer_list2}")
            msg_list = self.p1.statuses.pass_time()
            self.event_list.extend(msg_list)
            msg_list = self.p2.statuses.pass_time()
            self.event_list.extend(msg_list)
            print(f"HP p1: {self.p1.hp.value} / p2: {self.p2.hp.value}")
            self.state = game_states.BATTLE
            print("===========================================")
        
        for event in self.event_list:
            if type(event) is dict:
                msg = event
            else:
                msg = event.execute()
            print(f"{msg['msg']}")
        
        self.event_list = []


    

if __name__ == '__main__':
    game = Game()
    while True:
        game.main_loop()