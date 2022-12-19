from google.protobuf.json_format import MessageToDict

def get_total_craft(res):
    total_crafts = res.backup.artifacts_db.artifact_status
    return sum(el.count for el in total_crafts if ("GREATER" in str(el.spec) and "LUNAR_TOTEM" not in str(el.spec)) or (
                "TUNGSTEN_ANKH" in str(el.spec) and "NORMAL" in str(el.spec)))

def get_leg_number_total(res):
    inventory_items=res.backup.artifacts_db.inventory_items
    return sum(
        MessageToDict(el)["quantity"] for el in inventory_items if MessageToDict(el)["artifact"]["spec"]["rarity"]=="LEGENDARY")

def get_total_ships_exthens(res):
    ships = res.backup.artifacts_db.mission_archive
    return sum(
        1 for el in ships if "HENERPRISE" in str(el) and "EPIC" in str(el) and "ARCHIVED" in str(el))

def get_total_ships_standhens(res):
    ships = res.backup.artifacts_db.mission_archive
    return sum(
        1 for el in ships if "HENERPRISE" in str(el) and "LONG" in str(el) and "ARCHIVED" in str(el))

def get_total_ships_shens(res):
    ships = res.backup.artifacts_db.mission_archive
    return sum(
        1 for el in ships if "HENERPRISE" in str(el) and "SHORT" in str(el) and "ARCHIVED" in str(el))

def get_array_ships_ID(res): #not used
    ships = res.backup.artifacts_db.mission_archive
    return [el.identifier for el in ships if "HENERPRISE" in str(el) and "ARCHIVED" in str(el)]

def get_total_drop_exthens(res):
    ships = res.backup.artifacts_db.mission_archive
    return sum(el.capacity for el in ships if "HENERPRISE" in str(el) and "EPIC" in str(el) and "ARCHIVED" in str(el))

def formula_LLC(l_amount,total_craft,exhens,standards,shens):
    expected_drop_l = exhens / 25 + standards / (4.5 * 25) + shens / (6 * 25)
    expected_craft_l = total_craft * 0.0085

    print("Expected legendaries: " + str(expected_drop_l + expected_craft_l))
    print("Your legendaries: " + str(l_amount))
    return (l_amount - expected_drop_l - expected_craft_l)

#The methods below were used to get all the drop from all ships and check if there were a legendary,
#removed due to too many calls to the server

'''
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
'''