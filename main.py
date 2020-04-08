import misc.game_states as game_states
from misc.input_handlers import handle_action, handle_character_choice
import components.weapons as wpns

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
        self.actors = []
        self.equipments = [wpns.Dagger(), wpns.Zarabatana()]
        self.p1 = None
        self.p2 = None

    def main_loop(self):
        if self.state == game_states.START:
            ########################## STARTING SCREEN ONLY SHOWN ONCE
            choice = input(f"""{actor_choices} \nChoose p1 character: """)
            choice = choice if choice else 'tt'
            equip_num_choice = input(f"Equipments for P1 {self.show_equipments()}")
            equip_num_choice = int(equip_num_choice) if equip_num_choice else 1
            self.p1 = handle_character_choice(choice, equip_num_choice, self.equipments)
            choice = input(f"""\nChoose p2 character: """)
            choice = choice if choice else 'cg'
            equip_num_choice = input(f"Equipments for P2 {self.show_equipments()}")
            equip_num_choice = int(equip_num_choice) if equip_num_choice else 2
            self.p2 = handle_character_choice(choice, equip_num_choice, self.equipments)
            print(f"p1: {self.p1.name}-{self.p1.job.name}-{self.p1.equipment.name} VS p2: {self.p2.name}-{self.p2.job.name}-{self.p2.equipment.name}")
            self.state = game_states.BATTLE

            self.actors.extend([self.p1, self.p2])

        elif self.state is game_states.BATTLE:
            ######################### BATTLE SHOWN 
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

            comm_num_choice = input(f"""P1 {self.p1.show_commands()} \n""")
            comm_num_choice = int(comm_num_choice) if comm_num_choice else 1
            entity_num_choice = input(f"Targets for P1 {self.p1.name}: {self.show_actors()}")
            entity_num_choice = int(entity_num_choice) if entity_num_choice else 1
            action = handle_action(comm_num=comm_num_choice, owner=self.p1, 
            target_num=entity_num_choice, actors=self.actors)
            self.event_list.append(action)
            comm_num_choice = input(f"""P2 {self.p2.show_commands()} \n""")
            comm_num_choice = int(comm_num_choice) if comm_num_choice else 1
            entity_num_choice = input(f"Targets for P2 {self.p2.name}: {self.show_actors()}")
            entity_num_choice = int(entity_num_choice) if entity_num_choice else 1
            action = handle_action(comm_num=comm_num_choice, owner=self.p2, 
            target_num=entity_num_choice, actors=self.actors)
            self.event_list.append(action)
            self.state = game_states.PAUSE
            print("++++++++++++++++++++++++++++++++++++++++++++++")

        elif self.state is game_states.PAUSE:
            ############################### BATTLE RESULTS
            import pdb; pdb.set_trace()
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

            if msg:
                print(f"{msg.get('msg', f'no msg to show... {event}')}")
            else:
                print(f"{event}")
        self.event_list = []

    def show_actors(self):
        actor_str = ''
        i = 1
        for actor in self.actors:
            actor_str = actor_str + f'({i}) {actor.name}, '
            i += 1

        actor_str = actor_str[:-2] + '.'
        return actor_str

    def show_equipments(self):
        equip_str = ''
        i = 1
        for equip in self.equipments:
            equip_str = equip_str + f'({i}) {equip.name}, '
            i += 1

        equip_str = equip_str[:-2] + '.'
        return equip_str


if __name__ == '__main__':
    game = Game()
    while True:
        game.main_loop()