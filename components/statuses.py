import components.commands as com
import constants.status_cons as cons


class StatusList():
    def __init__(self):
        self.list = []

    def add_status(self, status):
        self.list.append(status)
        status.apply_buff()

    def remove_status(self, status): 
        status.remove_status()   
        self.list.remove(status)

    def pass_time(self):
        msg_list = []
        for status in self.list:
            msg = status.pass_time()
            msg_list.append(msg)
            if status.timer == 0:
                self.remove_status(status)
                msg = {"msg": f"{status.name} ran out"}
                msg_list.append(msg)

        return msg_list

class CommandStatusList():
    def __init__(self):
        self.list = []

    def init(self, statuses):
        for status in statuses:
            self.add_status(status)

    def add_status(self, status):
        self.list.append(status)

    def remove_status(self, status): 
        status.remove_status() 

class Status():
    def __init__(self, **kwargs):
        self.name = kwargs.get("name", "Curse of The Deep")
        self.base_name = kwargs.get("base_name", "Curse of The Deep")
        self.value = kwargs.get("value", 0)
        self.timer = kwargs.get("timer", 0)
        self.owner = kwargs.get("owner", None)
        self.target = kwargs.get("target", None)
        self.category = kwargs.get("category", "Deep")
        self.statuses = kwargs.get("statuses", [self]) if kwargs.get("statuses", False) else [self]

    def apply_buff(self):
        pass

    def pass_time(self):
        self.timer -= 1
        return {"msg": "Basic Status MSG, shouldn't be visible in normal circumstances"}

    def remove_status(self):
        pass

#BASE MAIN ARCHETYPES
class DoT(Status):
    def __init__(self, target=None, owner=None, name="Amaterasu", base_name="dot", value=0, timer=0, category='dot', statuses=[]):
        super().__init__(name=name, base_name=base_name, value=value, timer=timer, target=target, owner=owner, category=category, statuses=statuses)

    def pass_time(self):
        super().pass_time()
        com.Attack(owner=self.owner, target=self.target).deal_damage(damage=self.value, is_raw=True)
        return {"msg": f"Basic DoT msg, value = {self.value}, current_timer = {self.timer}"}

class HoT(Status):
    def __init__(self, target=None, owner=None, value=0, timer=0, base_name="hot", name="Seeds of Love", category='hot', statuses=[]):
        super().__init__(name=name, base_name=base_name, value=value, timer=timer, target=target, owner=owner, category=category, statuses=statuses)

    def pass_time(self):
        super().pass_time()
        com.Heal(owner=self.owner, target=self.target, value=self.value).execute()
        return {"msg": f"Basic HoT msg, value = {self.value}, current_timer = {self.timer}"}

class Buff(Status):
    def __init__(self, target=None, owner=None, name="Ronacse's Grace", base_name="buff", timer=0, statuses=[], category='buff', value=0, attr=None):
        super().__init__(name=name, base_name=base_name, value=value, timer=timer, target=target, owner=owner, category=category, statuses=statuses)
        self.attr = attr

    def apply_buff(self):
        
        for status in self.statuses:
            old_value = getattr(getattr(self.target, self.attr), 'value')
            setattr(getattr(self.target, self.attr), 'value', old_value + self.value)

    def pass_time(self):
        super().pass_time()
        return {"msg": f"{self.name} Pass Time"}

    def remove_status(self):
        for status in self.statuses:
            old_value = getattr(getattr(self.target, self.attr), 'value')
            setattr(getattr(self.target, self.attr), 'value', old_value - self.value)

        self.owner = None

################################        
####### SPECIAL STATUSES #######
################################

class Stunned(Status):
    def __init__(self, target=None, owner=None, base_name=cons.STUNNED["base_name"], timer=cons.STUNNED["timer"], value=0, name=cons.STUNNED["name"], 
    category=cons.STUNNED["category"], statuses=[]):
        super().__init__(name=name, base_name=base_name, timer=timer, target=target, owner=owner, category=category, value=value, statuses=statuses)

class PerfectCounterStance(Status):
    def __init__(self, target=None, owner=None, base_name=cons.PERFECT_COUNTER_STANCE["base_name"], timer=cons.PERFECT_COUNTER_STANCE["timer"], 
    value=0, name=cons.PERFECT_COUNTER_STANCE["name"], category=cons.PERFECT_COUNTER_STANCE["category"], statuses=[]):
        super().__init__(name=name, base_name=base_name, timer=timer, target=target, owner=owner, category=category, value=value, statuses=statuses)
        

def get_new_status_by_id(id, **kwargs):
    status = {
        "atk_up": Buff(**{**cons.ATK_UP, **kwargs}),
        "def_up": Buff(**{**cons.DEF_UP, **kwargs}),
        "spd_up": Buff(**{**cons.SPD_UP, **kwargs}),
        "max_hp_up": Buff(**{**cons.MAX_HP_UP, **kwargs}),
        "income_up": Buff(**{**cons.INCOME_UP, **kwargs}),
        "regen": HoT(**{**cons.REGENERATING, **kwargs}),
        "poisoned": DoT(**{**cons.POISONED, **kwargs}),
        "burned": HoT(**{**cons.BURNED, **kwargs}),
        "stunned": Stunned(**{**cons.STUNNED, **kwargs}),
        "perfect_counter_stance": PerfectCounterStance(**{**cons.PERFECT_COUNTER_STANCE, **kwargs}),
    }.get(id)

    return status
