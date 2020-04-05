import components.commands as com
import constants.status_constants as cons


class StatusList():
    def __init__(self):
        self.list = []

    def add_status(self, status):
        self.list.append(status)
        status.apply_buff()
        

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
                msg = {"msg": f"{s.name} ran out"}
                msg_list.append(msg)

        return msg_list



#VERY BASE OF ALL
class Status():
    def __init__(self, name="Curse of The Deep", value=0, timer=0, target=None, owner=None, category='The Deep'):
        self.name = name
        self.value = value
        self.timer = timer
        self.target = target
        self.owner = owner
        self.category = category

    def apply_buff(self):
        pass

    def pass_time(self):
        self.timer -= 1
        return {"msg": "Basic Status MSG, shouldn't be visible in normal circumstances"}

    def remove_status(self):
        pass

#BASE MAIN ARCHETYPES
class DoT(Status):
    def __init__(self, target=None, owner=None, name="Amaterasu", value=0, timer=0, category='dot'):
        super().__init__(name=name, value=value, timer=timer, target=target, owner=owner, category=category)

    def pass_time(self):
        super().pass_time()
        com.Attack(owner=self.owner, target=self.target, value=self.value, is_raw=True).execute()
        return {"msg": f"Basic DoT msg, value = {self.value}, current_timer = {self.timer}"}

class HoT(Status):
    def __init__(self, target=None, owner=None, value=0, timer=0, name="Seeds of Love", category='hot'):
        super().__init__(name=name, value=value, timer=timer, target=target, owner=owner, category=category)

    def pass_time(self):
        super().pass_time()
        com.Heal(owner=self.owner, target=self.target, value=self.value).execute()
        return {"msg": f"Basic HoT msg, value = {self.value}, current_timer = {self.timer}"}

class Buff(Status):
    def __init__(self, target=None, owner=None, name="Ronacse's Grace", timer=0, status_dict={}, category='buff'):
        super().__init__(name=name, value=0, timer=timer, target=target, owner=owner, category=category)
        self.status_dict = status_dict

    def apply_buff(self):
        for attr, value in self.status_dict.items():
            old_value = getattr(getattr(self.target, attr), 'value')
            setattr(getattr(self.target, attr), 'value', old_value + value)

    def pass_time(self):
        super().pass_time()
        return {"msg": f"{self.name} Pass Time"}

    def remove_status(self):
        for attr, value in self.status_dict.items():
            old_value = getattr(getattr(self.target, attr), 'value')
            setattr(getattr(self.target, attr), 'value', old_value - value)
        

#ACTUAL SPECIFIC STATUSES
class AtkUp(Buff):
    def __init__(self, target=None, owner=None, timer=cons.ATK_UP["timer"], name=cons.ATK_UP["name"], 
    status_dict=cons.ATK_UP["status_dict"], category=cons.ATK_UP["category"]):
        super().__init__(name=name, timer=timer, target=target, owner=owner, category=category, status_dict=status_dict)

    def remove_status(self):
        super().remove_status()

class DefUp(Buff):
    def __init__(self, target=None, owner=None, timer=cons.DEF_UP["timer"],
    name=cons.DEF_UP["name"], status_dict=cons.DEF_UP["status_dict"], category='buff'):
        super().__init__(name=name, timer=timer, target=target, owner=owner, category=category, status_dict=status_dict)

    def remove_status(self):
        super().remove_status()

class SpdUp(Buff):
    def __init__(self, target=None, owner=None, timer=cons.SPD_UP["timer"],
    name=cons.SPD_UP["name"], status_dict=cons.SPD_UP["status_dict"], category='buff'):
        super().__init__(name=name, timer=timer, target=target, owner=owner, category=category, status_dict=status_dict)

    def remove_status(self):
        super().remove_status()


class Regenerating(HoT):
    def __init__(self, target=None, owner=None, value=cons.REGENERATING["value"], timer=cons.REGENERATING["value"], 
    name=cons.REGENERATING["name"], category=cons.REGENERATING["category"]):
        super().__init__(name=name, value=value, timer=timer, target=target, owner=owner, category=category)
        
    def pass_time(self):
        super().pass_time()
        return {"msg": f"{self.target.name} heals {self.value} from Regen"}

class Poisoned(DoT):
    def __init__(self, target=None, owner=None, value=cons.POISONED["value"], timer=cons.POISONED["timer"], 
    name=cons.POISONED["name"], category=cons.POISONED["category"]):
        super().__init__(name=name, value=value, timer=timer, target=target, owner=owner, category=category)
        
    def pass_time(self):
        super().pass_time()
        return {"msg": f"{self.target.name} takes {self.value} to poison"}
