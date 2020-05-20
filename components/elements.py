class Element():
    def __init__(self,**kwargs):
        self.id = kwargs.get("id")
        self.name = kwargs.get("name", "Primal Element")
        self.timer = kwargs.get("timer", 0)
        
        from components.statuses import get_new_statuses_by_ids
        status_ids = kwargs.get("status_ids", [])
        self.statuses = get_new_statuses_by_ids(status_list=status_ids)
        

import constants.elements_cons as cons

def get_new_element_by_id(**kwargs):
    '''
    {
        "id": ,
        "name": ,
        "timer": ,
        "status_ids": [<status_id>]
    }
    '''
    elements = {
        "fire": Element(**{**cons.FIRE, **kwargs})
    }

    return elements.get(kwargs.get("id"))
