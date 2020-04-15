from components.commands import Command
import constants.equip_commands_cons as cons


class EquipEquipCommand(Command):
    def __init__(self, target=None, name="go equip an equip", 
    description="Getchoself an equip", category="equip_equip", equip=None):
        super().__init__(target=target,  name=name, description=description, category=category)
        self.equip = equip

    def execute(self):
        self.target.add_equip(self.equip)
        return {"msg": self.target.name + self.description}

class ZarabatanaCommand(EquipEquipCommand):
    def __init__(self, name=cons.ZARABATANA["name"], description=cons.ZARABATANA["description"], category=cons.ZARABATANA["category"], 
    equip=cons.ZARABATANA["equip"]):
        super().__init__(name=name, description=description, category=category, equip=equip)

    def execute(self):
        super().execute()

class DaggerCommand(EquipEquipCommand):
    def __init__(self, name=cons.DAGGER["name"], description=cons.DAGGER["description"], category=cons.DAGGER["category"], 
    equip=cons.DAGGER["equip"]):
        super().__init__(name=name, description=description, category=category, equip=equip)

    def execute(self):
        super().execute()

class CauldronCommand(EquipEquipCommand):
    def __init__(self, name=cons.CAULDRON["name"], description=cons.CAULDRON["description"], category=cons.CAULDRON["category"], 
    equip=cons.CAULDRON["equip"]):
        super().__init__(name=name, description=description, category=category, equip=equip)

    def execute(self):
        super().execute()

class ShieldCommand(EquipEquipCommand):
    def __init__(self, name=cons.SHIELD["name"], description=cons.SHIELD["description"], category=cons.SHIELD["category"], 
    equip=cons.SHIELD["equip"]):
        super().__init__(name=name, description=description, category=category, equip=equip)

    def execute(self):
        super().execute()

equips_list = [
    ZarabatanaCommand(),
    DaggerCommand(),
    CauldronCommand(),
    ShieldCommand(),
]