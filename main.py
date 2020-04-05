from components.commands import Attack, Heal, VampBite, PowerUp, Regen
import misc.game_states as game_states
from misc.input_handlers import handle_action, handle_character_choice

commands_options = """ choose an action:
    - Attack (a)
    - Heal (h)
    - ToxicShot (t)
    - VampBite (v)
    - PowerUp (p)
    - Regen (b)
    - SunCharge (s)\n"""

actor_choices = """ 
    Animals:
    - Turtle (t)
    - Fox (f)
    - Chicken (c)
    Jobs:
    - Guardian (g)
    - Thief (t)
    \n"""

class Game():
    def __init__(self):
        self.state = game_states.START
        self.log = []
        self.event_list = []
        self.entities = []
        self.p1 = None
        self.p2 = None

    def main_loop(self):
        if self.state == game_states.START:
            choice = input(f"""{actor_choices} \nChoose p1 character: """)
            self.p1 = handle_character_choice(choice)
            choice = input(f"""\nChoose p2 character: """)
            self.p2 = handle_character_choice(choice)
            print(f"p1: {self.p1.name}, the {self.p1.job.name} VS p2: {self.p2.name}, the {self.p2.job.name}")
            self.state = game_states.BATTLE

            self.entities.extend([self.p1, self.p2])

        elif self.state is game_states.BATTLE:
            print(f"""
            ++++++++++++++++++ BATTLE ++++++++++++++++++++++++++ 
            ----------------------------------------------------
            P1 - {self.p1.name}, the {self.p1.job.name} 
            HP: {self.p1.hp.value}/{self.p1.max_hp.value}
            ATK: {self.p1.atk_stat.value} 
            DEF: {self.p1.def_stat.value}
            SPD: {self.p1.spd_stat.value}
            Status: {self.p1.show_statuses()}
            Commands: {self.p1.show_commands()}
            ----------------------------------------------------
            P2 - {self.p2.name}, the {self.p2.job.name}
            HP: {self.p2.hp.value}/{self.p2.max_hp.value}
            ATK: {self.p2.atk_stat.value} 
            DEF: {self.p2.def_stat.value}
            SPD: {self.p2.spd_stat.value}
            Status: {self.p2.show_statuses()}
            Commands: {self.p2.show_commands()}
            ----------------------------------------------------
            """)

            comm_num_choice = int(input(f"""P1 {self.p1.show_commands()} \n"""))
            entity_num_choice = int(input(f"Targets: {self.show_entities()}"))
            action = handle_action(comm_num=comm_num_choice, owner=self.p1, 
            target_num=entity_num_choice, entities=self.entities)
            self.event_list.append(action)
            comm_num_choice = int(input(f"""P2 {self.p2.show_commands()} \n"""))
            entity_num_choice = int(input(f"Targets: {self.show_entities()}"))
            action = handle_action(comm_num=comm_num_choice, owner=self.p2, 
            target_num=entity_num_choice, entities=self.entities)
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

    def show_entities(self):
        entity_str = ''
        i = 1
        for entity in self.entities:
            entity_str = entity_str + f'({i}) {entity.name}, '
            i += 1

        entity_str = entity_str[:-2] + '.'
        return entity_str


if __name__ == '__main__':
    game = Game()
    while True:
        game.main_loop()