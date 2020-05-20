import constants.status_cons as cons

class StatusManager():
    def __init__(self):
        self.list = []

    def add_statuses_to_actor(self, statuses: list):       
        '''
            Recieves a list containing new instances of stati. If a given status
            is a buff (or debuff) it applies this buff to its owner.
        ''' 
        for status in statuses:
            status.owner = self.owner
            status.apply_buff()

        self.list.extend(statuses)

    def remove_status(self, status): 
        status.remove_status()   
        self.list.remove(status)

    def pass_time(self):
        '''
            All statuses are influenced by pass_time(), all statuses have their 
            timer attr diminished by 1.
        '''
        msg_list = []
        for status in self.list:
            msg = status.pass_time()
            msg_list.append(msg)
            if status.timer == 0:
                self.remove_status(status)
                msg = {"msg": f"{status.name} ran out"}
                msg_list.append(msg)

        return msg_list

    def show_statuses(self):
        '''
            Returns a string listing organizedly every status.
        '''
        statuses = ''
        for status in self.list:
            statuses += f'{status.name}({status.timer if status.timer >= 0 else "p"}), '

        statuses = statuses[:-2] + '.'
        return statuses

class ComponentStatusList():
    def __init__(self):
        self.list = []

    def add_statuses(self, statuses: list):
        for status in statuses:
            self.list.append(status)        

    def remove_status(self, status): 
        status.remove_status() 

    def add_statuses_ownership(self, statuses: list):
        for status in statuses:
            status.owner, status.target = self.owner, self.target

class PassivesList():
    def __init__(self):
        self.list = []

    def add_passive(self, passive):
        self.list.append(passive)

#########################################################################################
############################ MOTHER STATUS ##############################################
#########################################################################################

class Status():
    def __init__(self, **kwargs):
        self.id = kwargs.get("id")
        self.name = kwargs.get("name", "Curse of The Deep")
        self.base_name = kwargs.get("base_name", "Curse of The Deep")
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
        self.remove_buff()
        pass

    def remove_buff(self):
        pass

################################################################################################        
########################### BASE STATUSES ######################################################
################################################################################################

class DoT(Status):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def pass_time(self):
        super().pass_time()
        from components.commands import Attack
        Attack(owner=self.owner,
        target=self.target).deal_damage_to_target(damage=self.value, is_raw=True)
        return {"msg": f"Basic DoT msg, value = {self.value}, current_timer = {self.timer}"}

class HoT(Status):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def pass_time(self):
        super().pass_time()
        from components.commands import Heal
        Heal(owner=self.owner, target=self.target, value=self.value).heal_damage(self.value)
        return {"msg": f"Basic HoT msg, value = {self.value}, current_timer = {self.timer}"}

class Buff(Status):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.attr = kwargs.get("attr")

    def apply_buff(self):
        current_value = getattr(self.owner, self.attr)
        setattr(self.owner, self.attr, current_value + self.value)

    def remove_buff(self):
        
        current_value = getattr(self.owner, self.attr)
        setattr(self.owner, self.attr, current_value - self.value)
        self.owner = None

    def pass_time(self):
        super().pass_time()
        return {"msg": f"{self.name} Pass Time"}

################################################################################################        
################################ SPECIAL STATUSES ##############################################
################################################################################################

# Stunned
# Perfect Counter Stance

def get_status_obj_and_params(id_: str):
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
        "stunned": [Status, cons.STUNNED],
        "perfect_counter_stance": [Status, cons.PERFECT_COUNTER_STANCE],

        "atk_up": [Buff, cons.ATK_UP],
        "def_up": [Buff, cons.DEF_UP],
        "spd_up": [Buff, cons.SPD_UP],
        "max_hp_up": [Buff, cons.MAX_HP_UP],
        "income_up": [Buff, cons.INCOME_UP],
        
        "regen": [HoT, cons.REGENERATING],
        "poisoned": [DoT, cons.POISONED],
        "burned": [DoT, cons.BURNED],
    }

    return statuses.get(id_)

def get_new_statuses_by_ids(status_list: list = [])-> list:
    statuses = []

    for status_dict in status_list:
        obj, cons = get_status_obj_and_params(status_dict["id"])
        statuses.append(obj(**{**cons, **status_dict}))

    return statuses
