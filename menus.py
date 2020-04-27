from random import choice
from misc.entities_creation import create_actor, create_job, create_equip

def actors_options():
    creatures = {
        "Chicken": "c",
        "Fox": "f",
        "Turtle": "t",
        "Owl": "o",
        "Capybara": "p",
        "Alligator": "a",
    }
    jobs = {
        "Guardian": "g",
        "Thief": "t",
        "Cook": "c",
        "Hunter": "h",
        "Merchant": "m",
    }
    equips = {
        "Zarabatana": "z",
        "Dagger": "d",
        "Cauldron": "c",
        "Shield": "s",
    }

    c_list = list(creatures)
    j_list = list(jobs)
    e_list = list(equips)

    c = "Creatures"
    j = "Jobs"
    e = "Equipments"

    t_len_min = 11
    t_len_max = t_len_min + 3
    print(f"| {c + ' '*(t_len_max -len(c))}| {j +  ' '*(t_len_max -len(j))}| {e + ' '*(t_len_max - len(e))}|")
    print(f"{'-'*(t_len_max*3)}") 
    for i in range(max(len(c_list), len(j_list))):
        if(i < len(c_list)):
            print(f"| {c_list[i]}({creatures[c_list[i]]}){' '*(t_len_min-len(c_list[i]))}|", end="")
        else:
            print(f"| {' '*t_len_max}|", end="")

        if (i < len(j_list)):
            print(f" {j_list[i]}({jobs[j_list[i]]}){' '*(t_len_min-len(j_list[i]))}|", end="")
        else:
            print(f" {' '*t_len_max}|", end="")

        if (i < len(e_list)):
            print(f" {e_list[i]}({equips[e_list[i]]}){' '*(t_len_min-len(e_list[i]))}|")
        else:
            print(f" {' '*t_len_max}|")

    print(f"{'-'*(t_len_max*3)}") 


def initial_setup(initial_values, p1, p2, game):
    actors_num = initial_values["actors_num"]
    jobs_num = initial_values["jobs_num"]
    equips_num = initial_values["equips_num"]

    players = [p1, p2]

    # actors_options()

    for player in players:
        select_initial_actor_job_equip(player, actors_num, jobs_num, equips_num, game)




def select_initial_actor_job_equip(player, n_actors, n_jobs, n_equips, game):
    player_actors = []
    player_equips = []
    player_jobs = []
    actors_l = ["t", "f", "c", "a", "p", "o"]
    jobs_l = ["g", "t", "c", "h", "m"]
    equips_l = ["z", "d", "c", "s"]
    
    # p_choice = input(f"Actors ({n_actors}): ")
    actors =  "".join([choice(actors_l) for _ in range(n_actors)]) #p_choice if p_choice else
    actors = list(actors[:n_actors])
    for actor in actors:
        player.add_actor(create_actor(actor, game))

    # p_choice = input(f"Jobs ({n_jobs}): ")
    jobs =  "".join([choice(jobs_l) for _ in range(n_jobs)]) #p_choice if p_choice else
    jobs = list(jobs[:n_jobs])
    for job in jobs:
        player.add_job(create_job(job))

    # p_choice = input(f"Equips ({n_equips}): ")
    equips = "".join([choice(equips_l) for _ in range(n_equips)]) #p_choice if p_choice else 
    equips = list(equips[:n_equips])
    for equip in equips:
        player.add_equip(create_equip(equip))


def show_battle_stats(p1, p2):
    n_actors = len(p1.actors)
    players = [p1, p2]
    c_len = 14
    for p in players:
        for i in range(n_actors):
            name = p.actors[i].name
            print(f"| {name + ' '*(c_len - len(name))}", end="")
        print(f"|")

        for i in range(n_actors):
            hp = p.actors[i].hp.value
            max_hp = p.actors[i].max_hp.value
            both = "HP: "+str(hp)+ "/" + str(max_hp)
            print(f"| {both + ' '*(c_len - len(both))}", end="")
        print(f"|")

        for i in range(n_actors):
            atk = "ATK: " + str(p.actors[i].atk_stat.value)
            print(f"| {atk + ' '*(c_len - len(atk))}", end="")
        print(f"|")

        for i in range(n_actors):
            def_stat = "DEF: " + str(p.actors[i].def_stat.value)
            print(f"| {def_stat + ' '*(c_len - len(def_stat))}", end="")
        print(f"|")

        for i in range(n_actors):
            spd = "SPD: " + str(p.actors[i].spd_stat.value)
            print(f"| {spd + ' '*(c_len - len(spd))}", end="")
        print(f"|")

        for i in range(n_actors):
            income = "IN: " + str(p.actors[i].income_stat.value)
            print(f"| {income + ' '*(c_len - len(income))}", end="")
        print(f"|")

        for i in range(n_actors):
            equip = p.actors[i].job.name if p.actors[i].job else "No job"
            print(f"| {equip + ' '*(c_len - len(equip))}", end="")
        print(f"|")

        for i in range(n_actors):
            equip = p.actors[i].equip.name if p.actors[i].equip else "No item"
            print(f"| {equip + ' '*(c_len - len(equip))}", end="")
        print(f"|")

        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")