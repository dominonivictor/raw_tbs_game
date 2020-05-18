from components.actors import Actor

def get_new_actor(**kwargs):
    test = kwargs.get("test", False)

    if test:
        commands_ids = [
            "attack",
            "heal",
            "power_up",
            "rage",
            "speed_up",
            "regen",
            "toxic_shot",
            "defense_up",
            "vamp_bite",
            "speed_up",
        ]
        kwargs ={**kwargs, **{"commands_ids": commands_ids}}
    return Actor(**kwargs) 
