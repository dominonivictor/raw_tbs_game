class Element():
    def __init__(self, name="Primal Element", timer=0, status_dict={}):
        self.name = name
        self.timer = timer
        self.status_dict = status_dict

FIRE ={
    "name": "Fire",
    "timer": 4,
    "status_dict":{
        "burned": 25
    },
}

class Fire(Element):
    def __init__(self, name=FIRE["name"], timer=FIRE["timer"], status_dict=FIRE["status_dict"]):
        super().__init__(name=name, timer=timer, status_dict=status_dict)
