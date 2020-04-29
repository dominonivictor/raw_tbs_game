

class Element():
    def __init__(self, name="Primal Element", timer=0, statuses=[]):
        self.name = name
        self.timer = timer
        self.statuses = statuses


import constants.elements_cons as cons

def get_new_element_by_id(id):
    elements = {
        "fire": Element(**cons.FIRE)
    }

    return elements.get(id)