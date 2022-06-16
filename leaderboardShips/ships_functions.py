import json
from tqdm import tqdm
from google.protobuf.json_format import MessageToJson, MessageToDict


def __get_array_ships_ID__(res): #get all exthens IDs
    ships = res.backup.artifacts_db.mission_archive
    return [el.identifier for el in ships if "HENERPRISE" in str(el) and "EPIC" in str(el) and "ARCHIVED" in str(el)]

def loots(res,server_manager):
    file_loot=[]
    print("Please wait, DO NOT CLOSE THIS PAGE, maybe you can actually but please wait till the end and don't press STOP :)\n")
    print("If you are wondering why it's this slow it's because i don't want to spend some money on a server so replit is doing the job\n\n")
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

def __level_to_tier__(name, level_string):
    if "STONE" in name:
        if "FRAGMENT" in name:
            return 1
        elif level_string=="INFERIOR":
            return 2
        elif level_string == "LESSER":
            return 3
        elif level_string=="NORMAL":
            return 4
    else:
        return 1 if level_string=="INFERIOR" else 2 if level_string=="LESSER" \
            else 3 if level_string=="NORMAL" else 4 if level_string=="GREATER" else 0

def semplify_drop_list(list_drop):
    drops={}
    for el in list_drop:
        name=el["spec"]["name"]
        level=el["spec"]["level"]
        rarity=el["spec"]["rarity"]
        tier=str(__level_to_tier__(name,level))
        if name not in drops.keys():
            drops[name]={tier: {rarity:{"count":1}}}
        elif tier not in drops[name].keys():
            drops[name][tier] = {rarity:{"count":1}}
        elif rarity not in drops[name][tier].keys():
            drops[name][tier][rarity] = {"count":1}
        else:
            drops[name][tier][rarity]["count"]+=1
    return drops

def semplify_dict(file_dict):
    new_dict={}
    for el in file_dict:
        identifier=el["identifier"]
        stars=0
        try:
            stars=el["level"]
        except:
            pass
        drops=el["drop_List"]
        semplified_drops=semplify_drop_list(drops)
        new_dict[identifier]={"stars":stars,"drops":semplified_drops}
    return new_dict
