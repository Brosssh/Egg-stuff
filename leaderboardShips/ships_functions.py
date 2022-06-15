import json
from tqdm import tqdm
from google.protobuf.json_format import MessageToJson, MessageToDict


def __get_array_ships_ID__(res): #get all exthens IDs
    ships = res.backup.artifacts_db.mission_archive
    return [el.identifier for el in ships if "HENERPRISE" in str(el) and "EPIC" in str(el) and "ARCHIVED" in str(el)]

def loots(res,server_manager):
    file_loot=[]
    for el in tqdm(__get_array_ships_ID__(res)):
        ship_raw = server_manager.get_loot(el)
        ship_dict=(MessageToDict(ship_raw.info))
        n_drops=len(ship_raw.artifacts)
        drops=[]
        for i in range(n_drops):
            dict_temp=MessageToDict(ship_raw.artifacts[i])
            drops.append(dict_temp)
        ship_dict["drop_List"]=drops
        file_loot.append(ship_dict)
    return file_loot

def semplify_drop_list(list_drop):
    name_list=[]
    drops=[]
    for el in list_drop:
        name=el["spec"]["name"]
        level=el["spec"]["level"]
        rarity=el["spec"]["rarity"]
        if name not in name_list:
            name_list.append(name)
            drops.append({"name":name,"rarity":rarity,""})

def semplify_dict(file_dict):
    new_json=""
    for el in file_dict:
        seconds_remaining=el["secondsRemaining"]
        identifier=el["identifier"]
        stars=0
        try:
            stars=el["level"]
        except:
            pass
        drops=el["drop_List"]
        semplify_drop_list(drops)
    return seconds_remaining
