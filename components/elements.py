import constants.elements_constants as cons


class Element():
    def __init__(self, name="Primal Element", timer=0, status_dict={}):
        self.name = name
        self.timer = timer
        self.status_dict = status_dict



class Fire(Element):
    def __init__(self, name=cons.FIRE["name"], timer=cons.FIRE["timer"], status_dict=cons.FIRE["status_dict"]):
        super().__init__(name=name, timer=timer, status_dict=status_dict)
