import components.commands as com
import constants.status_cons as cons


class StatusList():
    def __init__(self):
        self.list = []

    def add_status(self, status):
        if type(status) is list:
            new_list = [get_new_status_by_id(**{**s.__dict__, **{"owner": self.owner}}) for s in status]
            self.list.extend(new_list)
            for status in new_list:
                status.apply_buff()
        else:
            new_status = get_new_status_by_id(**{**status.__dict__, **{"owner": self.owner}})
            self.list.append(new_status)
            new_status.apply_buff()

        print(f"owner:{self.owner.name}, statuses: {self.owner.statuses.list}")

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
            new_status = get_new_status_by_id(**status) if type(status) is not list else self.init(status)
            self.add_status(new_status)

    def add_status(self, status):
        if type(status) is list:
            for s in status:
                self.add_status(s)
        else:
            new_status = get_new_status_by_id(**status.__dict__)
            new_status.owner = self.owner
            self.list.append(new_status)

    def remove_status(self, status): 
        status.remove_status() 

class Status():
    def __init__(self, **kwargs):
        self.id = kwargs.get("id")
        self.name = kwargs.get("name", "Curse of The Deep")
        self.base_name = kwargs.get("base_name", "Curse of The Deep")
        self.attr = kwargs.get("attr")
        self.value = kwargs.get("value", 0)
        self.timer = kwargs.get("timer", 0)
        self.owner = kwargs.get("owner", None)
        self.target = kwargs.get("target", None)
        self.category = kwargs.get("category", "Deep")
        self.statuses = kwargs.get("statuses", [self]) if kwargs.get("statuses", []) else [self]

    def apply_buff(self):
        pass

    def pass_time(self):
        self.timer -= 1
        return {"msg": "Basic Status MSG, shouldn't be visible in normal circumstances"}

    def remove_status(self):
        pass

#BASE MAIN ARCHETYPES
class DoT(Status):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def pass_time(self):
        super().pass_time()
        com.Attack(owner=self.owner, target=self.target).deal_damage(damage=self.value, is_raw=True)
        return {"msg": f"Basic DoT msg, value = {self.value}, current_timer = {self.timer}"}

class HoT(Status):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def pass_time(self):
        super().pass_time()
        com.Heal(owner=self.owner, target=self.target, value=self.value).execute()
        return {"msg": f"Basic HoT msg, value = {self.value}, current_timer = {self.timer}"}

class Buff(Status):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

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
#Stunned
#PerfectCounterStance

def get_statuses_dict(**kwargs):
    """
    {
        "name":,
        "base_name": ,
        "value":,
        "timer":,
        "category":,
        "attr": ,#optional, if impacts an actor attr
    }
    """
    statuses = {
        "atk_up": Buff(**{**cons.ATK_UP, **kwargs}),
        "def_up": Buff(**{**cons.DEF_UP, **kwargs}),
        "spd_up": Buff(**{**cons.SPD_UP, **kwargs}),
        "max_hp_up": Buff(**{**cons.MAX_HP_UP, **kwargs}),
        "income_up": Buff(**{**cons.INCOME_UP, **kwargs}),
        "regen": HoT(**{**cons.REGENERATING, **kwargs}),
        "poisoned": DoT(**{**cons.POISONED, **kwargs}),
        "burned": DoT(**{**cons.BURNED, **kwargs}),
        "stunned": Status(**{**cons.STUNNED, **kwargs}),
        "perfect_counter_stance": Status(**{**cons.PERFECT_COUNTER_STANCE, **kwargs}),
    }

    return statuses

def get_new_status_by_id(**kwargs):
    id = kwargs.get("id")
    status = get_statuses_dict(**kwargs).get(id)

    return status
