from components.jobs import Job
from components.commands import get_new_commands_by_ids
import constants.job_cons as con

def get_new_job(job_id):
    job = {
        "guardian": con.GUARDIAN,
        "thief": con.THIEF,
        "cook": con.COOK,
        "merchant": con.MERCHANT,
        "hunter": con.HUNTER
    }.get(job_id)

    job["commands"] = get_new_commands_by_ids(command_ids=job["commands_ids"])
    #should it send the StatusList, CommandsList and stuff...
    
    return Job(**job) 
