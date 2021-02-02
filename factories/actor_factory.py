from components.actors import Actor


def get_new_actor(**kwargs):
    test = kwargs.get("test", False)

    if test:
        # This list follows exactly the commands.py commands_dict
        # duplication in this case is dangerous, if i mistype or forget
        # it will bite me later...
        commands_ids = [
            # BASICS
            "attack",
            "heal",
            "vamp_bite",
            # KINGDOM
            "sun_charge",
            "golden_egg",
            "multiply",
            # JOBS
            "perfect_counter",
            "copy_cat",
            "mixn",
            # EQUIPS
            "true_slash",
            "toxic_shot",
            "shield_bash",
            "rage",
            "paralize_shot",
            # STATUSES
            "power_up",
            "defense_up",
            "speed_up",
            "regen",
            # AOE
            "waterball",
        ]
        kwargs = {**kwargs, **{"commands_ids": commands_ids}}
    return Actor(**kwargs)
