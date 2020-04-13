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

class Status():
    def __init__(self, name="Curse of The Deep", base_name="Curse of The Deep", value=0, timer=0, target=None, owner=None, 
    category='The Deep', status_dict={}):
        self.name = name
        self.base_name = base_name
        self.value = value
        self.timer = timer
        self.owner = owner
        self.target = target
        self.category = category
        self.status_dict = status_dict

    def apply_buff(self):
        pass

    def pass_time(self):
        self.timer -= 1
        return {"msg": "Basic Status MSG, shouldn't be visible in normal circumstances"}

    def remove_status(self):
        pass


class Stunned(Status):
    def __init__(self, target=None, owner=None, base_name=cons.STUNNED["base_name"], timer=cons.STUNNED["timer"], value=0, name=cons.STUNNED["name"], 
    category=cons.STUNNED["category"], status_dict={}):
        super().__init__(name=name, base_name=base_name, timer=timer, target=target, owner=owner, category=category, value=value, status_dict=status_dict)

class PerfectCounterStance(Status):
    def __init__(self, target=None, owner=None, base_name=cons.PERFECT_COUNTER_STANCE["base_name"], timer=cons.PERFECT_COUNTER_STANCE["timer"], 
    value=0, name=cons.PERFECT_COUNTER_STANCE["name"], category=cons.PERFECT_COUNTER_STANCE["category"], status_dict={}):
        super().__init__(name=name, base_name=base_name, timer=timer, target=target, owner=owner, category=category, value=value, status_dict=status_dict)


#BASE MAIN ARCHETYPES
class DoT(Status):
    def __init__(self, target=None, owner=None, name="Amaterasu", base_name="dot", value=0, timer=0, category='dot', status_dict={}):
        super().__init__(name=name, base_name=base_name, value=value, timer=timer, target=target, owner=owner, category=category, status_dict=status_dict)

    def pass_time(self):
        super().pass_time()
        com.Attack(owner=self.owner, target=self.target).deal_damage(damage=self.value)
        return {"msg": f"Basic DoT msg, value = {self.value}, current_timer = {self.timer}"}

class HoT(Status):
    def __init__(self, target=None, owner=None, value=0, timer=0, base_name="hot", name="Seeds of Love", category='hot', status_dict={}):
        super().__init__(name=name, base_name=base_name, value=value, timer=timer, target=target, owner=owner, category=category, status_dict=status_dict)

    def pass_time(self):
        super().pass_time()
        com.Heal(owner=self.owner, target=self.target, value=self.value).execute()
        return {"msg": f"Basic HoT msg, value = {self.value}, current_timer = {self.timer}"}

class Buff(Status):
    def __init__(self, target=None, owner=None, name="Ronacse's Grace", base_name="buff", timer=0, status_dict={}, category='buff', value=0):
        super().__init__(name=name, base_name=base_name, value=value, timer=timer, target=target, owner=owner, category=category, status_dict=status_dict)

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
    def __init__(self, target=None, base_name=cons.ATK_UP["base_name"], owner=None, timer=cons.ATK_UP["timer"], value=0, name=cons.ATK_UP["name"], 
    status_dict=cons.ATK_UP["status_dict"], category=cons.ATK_UP["category"]):
        super().__init__(name=name, base_name=base_name, timer=timer, target=target, owner=owner, category=category, 
        status_dict=status_dict, value=value)

    def remove_status(self):
        super().remove_status()

class DefUp(Buff):
    def __init__(self, target=None, base_name=cons.DEF_UP["base_name"], owner=None, timer=cons.DEF_UP["timer"], value=0,
    name=cons.DEF_UP["name"], status_dict=cons.DEF_UP["status_dict"], category='buff'):
        super().__init__(name=name, base_name=base_name, timer=timer, target=target, owner=owner, category=category, 
        status_dict=status_dict, value=value)

    def remove_status(self):
        super().remove_status()

class SpdUp(Buff):
    def __init__(self, target=None, base_name=cons.SPD_UP["base_name"], owner=None, timer=cons.SPD_UP["timer"], value=0,
    name=cons.SPD_UP["name"], status_dict=cons.SPD_UP["status_dict"], category='buff'):
        super().__init__(name=name, base_name=base_name, timer=timer, target=target, owner=owner, category=category, 
        status_dict=status_dict, value=value)

    def remove_status(self):
        super().remove_status()

class MaxHpUp(Buff):
    def __init__(self, target=None, base_name=cons.MAX_HP_UP["base_name"], owner=None, timer=cons.MAX_HP_UP["timer"], value=0,
    name=cons.MAX_HP_UP["name"], status_dict=cons.MAX_HP_UP["status_dict"], category='buff'):
        super().__init__(name=name, base_name=base_name, timer=timer, target=target, owner=owner, category=category, 
        status_dict=status_dict, value=value)

    def remove_status(self):
        super().remove_status()

class IncomeUp(Buff):
    def __init__(self, target=None, base_name=cons.INCOME_UP["base_name"], owner=None, timer=cons.INCOME_UP["timer"], value=0,
    name=cons.INCOME_UP["name"], status_dict=cons.INCOME_UP["status_dict"], category='buff'):
        super().__init__(name=name, base_name=base_name, timer=timer, target=target, owner=owner, category=category, 
        status_dict=status_dict, value=value)

    def remove_status(self):
        super().remove_status()

class Enraged(Buff):
    def __init__(self, target=None, base_name=cons.ENRAGED["base_name"], owner=None, timer=cons.ENRAGED["timer"], value=0, name=cons.ENRAGED["name"], 
    status_dict=cons.ENRAGED["status_dict"], category=cons.ENRAGED["category"]):
        super().__init__(name=name, base_name=base_name, timer=timer, target=target, owner=owner, category=category, 
        status_dict=status_dict, value=value)

    def remove_status(self):
        super().remove_status()


class Regenerating(HoT):
    def __init__(self, target=None, base_name=cons.REGENERATING["base_name"], owner=None, value=cons.REGENERATING["value"], timer=cons.REGENERATING["value"], 
    name=cons.REGENERATING["name"], category=cons.REGENERATING["category"], status_dict={}):
        super().__init__(name=name, base_name=base_name, value=value, timer=timer, target=target, owner=owner, category=category,
        status_dict=status_dict)
        
    def pass_time(self):
        super().pass_time()
        return {"msg": f"{self.target.name} heals {self.value} from Regen"}

class Poisoned(DoT):
    def __init__(self, target=None, base_name=cons.POISONED["base_name"], owner=None, value=cons.POISONED["value"], timer=cons.POISONED["timer"], 
    name=cons.POISONED["name"], category=cons.POISONED["category"], status_dict={}):
        super().__init__(name=name, base_name=base_name, value=value, timer=timer, target=target, owner=owner, category=category, status_dict=status_dict)
        
    def pass_time(self):
        super().pass_time()
        return {"msg": f"{self.target.name} takes {self.value} to poison"}

class Burned(DoT):
    def __init__(self, target=None, base_name=cons.BURNED["base_name"], owner=None, value=cons.BURNED["value"], timer=cons.BURNED["timer"], 
    name=cons.BURNED["name"], category=cons.BURNED["category"], status_dict={}):
        super().__init__(name=name, base_name=base_name, value=value, timer=timer, target=target, owner=owner, category=category, status_dict=status_dict)
        
    def pass_time(self):
        super().pass_time()
        return {"msg": f"{self.target.name} takes {self.value} to THE BURN"}