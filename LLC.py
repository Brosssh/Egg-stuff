import threading
from tqdm import tqdm
from multiprocessing import Queue

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

def __split__(array, n_chunk):
    k, m = divmod(len(array), n_chunk)
    return list((array[i*k+min(i, m):(i+1)*k+min(i+1, m)] for i in range(n_chunk)))

def __execute_thread__(server_manager,array_thread,queue):
    legendary_count=0
    for el in array_thread:
        loot_response=server_manager.get_loot(el)
        if not loot_response:
            return "Something went wrong"
        elif "LEGENDARY" in str(loot_response):
            legendary_count+=1
    queue.put(legendary_count)

def get_leg_number_ships(res,server_manager):
    array_ships_ID=get_array_ships_ID(res)
    legendary_count=0
    q = Queue()
    matrix_from_array = __split__(array_ships_ID,4)
    if len(array_ships_ID)>4:

        t1 = threading.Thread(target=__execute_thread__, args=(server_manager,matrix_from_array[0],q,))
        t2 = threading.Thread(target=__execute_thread__, args=(server_manager,matrix_from_array[1],q,))
        t3 = threading.Thread(target=__execute_thread__, args=(server_manager,matrix_from_array[2],q,))
        t4 = threading.Thread(target=__execute_thread__, args=(server_manager,matrix_from_array[3],q,))

        t1.start()
        t2.start()
        t3.start()
        t4.start()

        # wait until threads are completely executed
        t1.join()
        t2.join()
        t3.join()
        t4.join()

        r1=q.get()
        r2=q.get()
        r3=q.get()
        r4=q.get()


        return sum([r1,r2,r3,r4])