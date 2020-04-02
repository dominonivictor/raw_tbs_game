from command

class StatusList():
    def __init__(self):
        self.list = []

    def add_status(self, status):
        status.owner = self
        self.list.append(status)

    def _remove_status(self, status):    
        self.list.remove(status)

    def pass_time(self):
        for s in self.list:
            s.timer -= 1
            if s.timer == 0:
                self._remove_status(s)

class Status():
    def __init__(self, name, value, timer):
        self.name = name
        self.value = value
        self.timer = timer

    def pass_time(self):
        self.timer -= 1

class Poison(Status):
    def __init__(self, name, value, timer):
        super().__init__(name, value, timer)

    def execute(self):
        target = self.owner.owner
        

    