def special_status_handler(command):
    owner_status_base_names, target_status_base_names = [], []
    if command.owner:
        owner_status_base_names = list(
            map(lambda c: c.get_base_name(), command.owner.statuses.list)
        )
    if command.target:
        target_status_base_names = list(
            map(lambda c: c.get_base_name(), command.target.statuses.list)
        )

    if "stunned" in owner_status_base_names:
        return stunned_handler(command)
    if "perfect_counter_stance" in target_status_base_names:
        perfect_counter_stance_handler(command)

    return {}


def stunned_handler(command):
    return {
        "msg": f"{command.owner.name} is stunned and can't move!",
        "valid_action": False,
        "result": {"attack": "no attack", "final_value": 0},
        "should_continue": False,
    }


def perfect_counter_stance_handler(command):
    command.set_target(command.owner)
