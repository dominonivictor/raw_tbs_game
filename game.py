import misc.game_states as game_states
from menus import initial_setup, show_battle_stats
import components.weapons as wpns
from player import Player


class Game():
    def __init__(self):
        self.state = game_states.START
        self.log = []
        self.event_list = []
        self.actors = []
        self.initial_values = {
            "actors_num": 2,
            "jobs_num": 2,
            "equips_num": 2
        }
        self.p1 = Player(name='P1')
        self.p2 = Player(name='P2')
        initial_setup(self.initial_values, p1=self.p1, p2=self.p2)
        self.add_actors()

    def main_loop(self):
        
        if self.state == game_states.START:
            
            initial_setup(self.initial_values, p1=self.p1, p2=self.p2)
        
            self.state = game_states.BATTLE

            self.add_actors()
            
            import pdb; pdb.set_trace()
        elif self.state is game_states.BATTLE:
            ######################### BATTLE SHOWN 
            show_battle_stats(self.p1, self.p2)

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

    def add_actors(self):
        p1_actors = [actor for actor in self.p1.actors]
        p2_actors = [actor for actor in self.p2.actors]
        self.actors.extend(p1_actors)
        self.actors.extend(p2_actors)


if __name__ == '__main__':
    game = Game()
    while True:
        game.main_loop()