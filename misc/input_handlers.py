
def handle_action(comm_num, owner, target_num, actors):
    # action shall come as a number indicating 
    comm_num -= 1
    target_num -= 1
    command = owner.commands.list[comm_num]
    command.target = actors[target_num]
    return command
    

commands_options = """ choose an action:
                - Attack (a)
                - Heal (h)
                - Toxic Shot (t)
                - Vamp Bite (v)
                - Power Up (p)
                - Regen (b)
                """