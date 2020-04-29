from components.commands import Command
import constants.equip_commands_cons as cons



class EquipEquipCommand(Command):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        from components.equips import get_new_equip_by_id
        equip = get_new_equip_by_id(id=kwargs.get("equip_id", None))
        self.equip = equip

    def execute(self):
        self.target.add_equip(self.equip)
        return {"msg": self.target.name + self.description}

def gen_equips_list():
    return [
        EquipEquipCommand(**cons.ZARABATANA),
        EquipEquipCommand(**cons.DAGGER),
        EquipEquipCommand(**cons.CAULDRON),
        EquipEquipCommand(**cons.SHIELD),
    ]