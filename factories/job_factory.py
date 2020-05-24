from components.jobs import Job

def get_new_job(job_id):
    job_dict = {
        "guardian": con.GUARDIAN,
        "thief": con.THIEF,
        "cook": con.COOK,
        "merchant": con.MERCHANT,
        "hunter": con.HUNTER
    }

    job = job_dict.get(job_id)

    job["commands"] = get_commands_by_ids(job["commands_ids"])
    #should it send the StatusList, CommandsList and stuff...
    
    return Job(**job) 
