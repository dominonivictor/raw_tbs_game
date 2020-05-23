from components.actors import Actor

def get_new_actor(**kwargs):
    test = kwargs.get("test", False)

    if test:
        #This list follows exactly the commands.py commands_dict
        #duplication in this case is dangerous, if i mistype or forget
        #it will bite me later...
        commands_ids = [

            "attack",
            "heal",
            "vamp_bite",
            
            "sun_charge",
            "golden_egg",
            "multiply",

            "perfect_counter",
            "copy_cat",
            "mixn",
            
            "true_slash",
            "toxic_shot",
            "shield_bash",
            "rage",
            "paralize_shot",

            "power_up",
            "defense_up",
            "speed_up",
            "regen",
        ]
        kwargs ={**kwargs, **{"commands_ids": commands_ids}}
    return Actor(**kwargs) 
