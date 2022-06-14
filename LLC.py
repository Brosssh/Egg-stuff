from tqdm import tqdm

def get_total_craft(res):
    total_crafts = res.backup.artifacts_db.crafting_counts
    return sum(el.count for el in total_crafts if ("GREATER" in str(el.spec) and "LUNAR_TOTEM" not in str(el.spec)) or (
                "TUNGSTEN_ANKH" in str(el.spec) and "NORMAL" in str(el.spec)))

def get_leg_number_total(res):
    inventory_items=res.backup.artifacts_db.inventory_items
    return sum(
        el.count for el in inventory_items if "LEGENDARY" in str(el.artifact.spec.rarity))

def get_total_ships(res):
    ships = res.backup.artifacts_db.mission_archive
    return sum(
        1 for el in ships if "HENERPRISE" in str(el) and "EPIC" in str(el) and "ARCHIVED" in str(el))

def get_array_ships_ID(res):
    ships = res.backup.artifacts_db.mission_archive
    return [el.identifier for el in ships if "HENERPRISE" in str(el) and "EPIC" in str(el) and "ARCHIVED" in str(el)]

def get_leg_number_ships(res,server_manager):
    array_ships_ID=get_array_ships_ID(res)
    legendary_count=0
    for el in tqdm(array_ships_ID):
        loot_response=server_manager.get_loot(el)
        if not loot_response:
            return "Something went wrong"
        elif "LEGENDARY" in str(loot_response):
            legendary_count+=1
    return legendary_count