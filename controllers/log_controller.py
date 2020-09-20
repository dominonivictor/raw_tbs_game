from kivy.app import App

def add_msg(msg="", msg_dict={}):
    if msg_dict:
        msg = msg_dict["msg"]

    app = App.get_running_instance()
    log_screen = app.root.ids.log_screen

def show_actor_stats(actor):
    '''Recieves actor and returns string representing stats'''

    return actor.show_battle_stats() if actor else "No actor selected"
