class Element():
    def __init__(self,**kwargs):
        self.id = kwargs.get("id")
        self.name = kwargs.get("name", "Primal Element")
        self.timer = kwargs.get("timer", 0)
        
        from components.statuses import get_new_status_by_id
        statuses = kwargs.get("statuses_func_params")
        self.statuses = [get_new_status_by_id(id=statuses)]
        

import constants.elements_cons as cons

def get_new_element_by_id(**kwargs):
    '''
    {
        "id": ,
        "name": ,
        "timer": ,
        "status_id": <status_id>
    }
    '''
    elements = {
        "fire": Element(**{**cons.FIRE, **kwargs})
    }

    return elements.get(kwargs.get("id"))