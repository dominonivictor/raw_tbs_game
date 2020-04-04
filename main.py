from commands import Attack, Heal, VampBite, PowerUp, Blessing
import game_states
from input_handlers import handle_action, handle_character_choice

commands_options = """ choose an action:
                - Attack (a)
                - Heal (h)
                - Toxic Shot (t)
                - Vamp Bite (v)
                - Power Up (p)
                - Blessing (b)
                - Sun Charge (s)
                """

actor_choices = """ 
                - Turtle (t)
                - Fox (f)
                - Chicken (c)\n\n"""

class Game():
    def __init__(self):
        self.state = game_states.START
        self.log = []
        self.event_list = []
        self.p1 = None
        self.p2 = None

    def main_loop(self):
        if self.state == game_states.START:
            choice = input(f"""Welcome, choose p1 character: {actor_choices} """)
            self.p1 = handle_character_choice(choice)
            choice = input(f"""Welcome, choose p2 character: {actor_choices}""")
            self.p2 = handle_character_choice(choice)
            print(f"p1: {self.p1.name} VS p2: {self.p2.name}")
            self.state = game_states.BATTLE

        elif self.state is game_states.BATTLE:
            print("++++++++++++++++ BATTLE ++++++++++++++++++++++")
            print(f""" 
            ----------------------------------------------------
            P1 - {self.p1.name} 
            HP: {self.p1.hp.value}/{self.p1.max_hp.value}
            ATK: {self.p1.atk_stat.value} 
            DEF: {self.p1.def_stat.value}
            SPD: {self.p1.spd_stat.value}
            Status: {self.p1.show_statuses()}
            Skills: {self.p1.show_commands()}
            ----------------------------------------------------
            P2 - {self.p2.name} 
            HP: {self.p2.hp.value}/{self.p2.max_hp.value}
            ATK: {self.p2.atk_stat.value} 
            DEF: {self.p2.def_stat.value}
            SPD: {self.p2.spd_stat.value}
            Status: {self.p2.show_statuses()}
            Skills: {self.p2.show_commands()}
            ----------------------------------------------------
            """)

            choice = input(f"""P1 {commands_options}""")
            action = handle_action(choice, owner=self.p1, target=self.p2)
            self.event_list.append(action)
            choice = input(f"""P2 {commands_options}""")
            action = handle_action(choice, owner=self.p2, target=self.p1)
            self.event_list.append(action)
            self.state = game_states.PAUSE
            print("++++++++++++++++++++++++++++++++++++++++++++++")

        elif self.state is game_states.PAUSE:
            print("========== IN BETWEEN TURNS ===============")
            msg_list = self.p1.statuses.pass_time()
            self.event_list.extend(msg_list)
            msg_list = self.p2.statuses.pass_time()
            self.event_list.extend(msg_list)
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