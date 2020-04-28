from random import choice
from misc.entities_creation import create_actor, create_job, create_equip


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

