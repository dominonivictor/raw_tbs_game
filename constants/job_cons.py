owner=None, 
owner=None, name="Thief", category="DPS/Utility", commands=[CopyCat(**comm_cons.COPY_CAT)], passives=[get_new_statuses_by_ids(ids_list=["spd_up"])]
owner=None, name="Hunter", category="DPS/Tank", commands=[Attack(**comm_cons.TOXIC_SHOT)], passives=[get_new_statuses_by_ids(ids_list=["atk_up"])]
owner=None, name="Cook", category="Utility/Tank", commands=[Mixn(**comm_cons.MIXN)], passives=[get_new_statuses_by_ids(ids_list=["max_hp_up"])]
owner=None, name="Merchant", category="Utility/DPS", commands=[Attack(**comm_cons.TOXIC_SHOT)], passives=[get_new_statuses_by_ids(ids_list=["income_up"])]

GUARDIAN ={
    "name": "Guardian", 
    "category": "Tank/Utility", 
    "commands_ids": ["perfect_counter"], 
    "status_ids": ["def_up"],
}