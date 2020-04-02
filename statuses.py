import commands as com


class StatusList():
    def __init__(self):
        self.list = []

    def add_status(self, status):
        status.owner = self
        self.list.append(status)

    def _remove_status(self, status): 
        status.remove_status()   
        self.list.remove(status)

    def pass_time(self):
        msg_list = []
        for s in self.list:
            msg = s.pass_time()
            msg_list.append(msg)
            if s.timer == 0:
                self._remove_status(s)
                msg = {"msg": "poison ran out"}
                msg_list.append(msg)

        return msg_list

#VERY BASE OF ALL
class Status():
    def __init__(self, name, value, timer, target, owner=None, category='no category'):
        self.name = name
        self.value = value
        self.timer = timer
        self.target = target
        self.owner = owner
        self.category = category

    def pass_time(self):
        self.timer -= 1
        return {"msg": "Basic Status MSG, shouldn't be visible in normal circumstances"}

    def remove_status(self):
        pass

#BASE MAIN ARCHETYPES
class DoT(Status):
    def __init__(self, name, value, timer, target, owner, category='dot'):
        super().__init__(name=name, value=value, timer=timer, target=target, owner=owner, category=category)

    def pass_time(self):
        super().pass_time()
        com.Attack(owner=self.owner, target=self.target, value=self.value).execute()
        return {"msg": f"Basic DoT msg, value = {self.value}, current_timer = {self.timer}"}

class HoT(Status):
    def __init__(self, value, timer, target, owner, name, category='hot'):
        super().__init__(name=name, value=value, timer=timer, target=target, owner=owner, category=category)

    def pass_time(self):
        super().pass_time()
        com.Heal(owner=self.owner, target=self.target, value=self.value).execute()
        return {"msg": f"Basic HoT msg, value = {self.value}, current_timer = {self.timer}"}

class Buff(Status):
    def __init__(self, name, timer, target, owner, attr_dict, value=0, category='buff'):
        super().__init__(name=name, value=value, timer=timer, target=target, owner=owner, category=category)
        self.attr_dict = attr_dict
        for attr, value in self.attr_dict.items():
            old_value = getattr(getattr(self.target, attr), 'value')
            setattr(getattr(self.target, attr), 'value', old_value + value)

    def pass_time(self):
        super().pass_time()
        return {"msg": "Buff Pass Time"}

    def remove_status(self):
        for attr, value in self.attr_dict.items():
            old_value = getattr(getattr(self.target, attr), 'value')
            setattr(getattr(self.target, attr), 'value', old_value - value)
        

#ACTUAL SPECIFIC STATUSES
class AtkUp(Buff):
    def __init__(self, timer, target, owner, name='atk up', attr_dict={"timer": 3,"atk_stat": 5}, category='buff'):
        super().__init__(name=name, timer=timer, target=target, owner=owner, category=category, attr_dict=attr_dict)

    def remove_status(self):
        super().remove_status()

class DefUp(Buff):
    def __init__(self, timer, target, owner, name='def up', attr_dict={"def_stat": 5}, category='buff'):
        super().__init__(name=name, timer=timer, target=target, owner=owner, category=category, attr_dict=attr_dict)

    def remove_status(self):
        super().remove_status()

class SpdUp(Buff):
    pass


class Regen(HoT):
    def __init__(self, value, timer, target, owner, name='regen', category='hot'):
        super().__init__(name=name, value=value, timer=timer, target=target, owner=owner, category=category)
        
    def pass_time(self):
        super().pass_time()
        return {"msg": f"{self.target.name} heals {self.value} from Regen"}

class Poisoned(DoT):
    def __init__(self, value, timer, target, owner, name='poison', category='dot'):
        super().__init__(name=name, value=value, timer=timer, target=target, owner=owner, category=category)
        
    def pass_time(self):
        super().pass_time()
        return {"msg": f"{self.target.name} takes {self.value} to poison"}
