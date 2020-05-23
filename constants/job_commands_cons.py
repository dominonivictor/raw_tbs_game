import components.jobs as jobs
import constants.job_cons as cons
#TODO this is wrong cause the instances are static...
BASE = {
    "name": "go get a job",
    "description": "Getchoself a job",
    "category": "learn_job",
    "job": None
}

GUARDIAN = {
    "name": "Guardian",
    "description": " became a Guardian, + def and stuff",
    "category": "learn_job",
    "job": jobs.Guardian(**cons.GUARDIAN)
}

THIEF = {
    "name": "Thief",
    "description": " became a Thief, + spd and stuff",
    "category": "learn_job",
    "job": jobs.Thief(**cons.THIEF),
}

MERCHANT = {
    "name": "Merchant",
    "description": " became a Merchant, + money and stuff",
    "category": "learn_job",
    "job": jobs.Merchant(**cons.MERCHANT),
}

HUNTER = {
    "name": "Hunter",
    "description": " became a Hunter, + offensive skills and stuff",
    "category": "learn_job",
    "job": jobs.Hunter(**cons.HUNTER),
}

COOK = {
    "name": "Cook",
    "description": " became a Cook, mixin and brewing",
    "category": "learn_job",
    "job": jobs.Cook(**cons.COOK),
}


'''
    "name": ,
    "description": ,
    "category": "learn_job",
    "job": ,
'''
