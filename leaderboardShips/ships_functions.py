import json
from tqdm import tqdm
from google.protobuf.json_format import MessageToJson, MessageToDict
import copy


def __get_array_ships_ID__(res): #get all exthens IDs
    ships = res.backup.artifacts_db.mission_archive
    return [el.identifier for el in ships if "HENERPRISE" in str(el) and "EPIC" in str(el) and "ARCHIVED" in str(el)]

def loots(res,server_manager):
    file_loot=[]
    #temp
    c=0
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
        c+=1
        #temp
        if c>=4:
            break
        # temp
        # temp



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
        capacity = el["capacity"]
        stars=0
        try:
            stars=el["level"]
        except:
            pass
        drops=el["drop_List"]
        semplified_drops=semplify_drop_list(drops)
        new_dict.append({"identifier":identifier,"stars":stars,"capacity":capacity, "drops":semplified_drops})
    return new_dict


#this code below is shit, need to be fixed
def check_and_update_file(old_leaderboard_l_dict,array_new_gold):
    new_leaderboard_l_dict=old_leaderboard_l_dict
    array_new_gold=sorted(array_new_gold, key=lambda item: item.get("total"))
    for el in array_new_gold[-3:]:
        #par
        if new_leaderboard_l_dict["1"]["count"][0]["total"]==el["total"]:
            new_leaderboard_l_dict["1"]["info"]["name"].append(el["info"]["name"])
            new_leaderboard_l_dict["1"]["info"]["stars"].append(el["info"]["stars"])
        elif new_leaderboard_l_dict["2"]["count"][0]["total"]==el["total"]:
            new_leaderboard_l_dict["2"]["count"].append(el["total"])
            new_leaderboard_l_dict["2"]["info"]["name"].append(el["info"]["name"])
            new_leaderboard_l_dict["2"]["info"]["stars"].append(el["info"]["stars"])
        elif new_leaderboard_l_dict["3"]["count"][0]["total"]==el["total"]:
            new_leaderboard_l_dict["3"]["info"]["name"].append(el["info"]["name"])
            new_leaderboard_l_dict["3"]["info"]["stars"].append(el["info"]["stars"])

        elif el["total"]>new_leaderboard_l_dict["1"]["count"][0]["total"]:

            #if the 1 is new, old 1 become 2 and old 2 second 3
            new_leaderboard_l_dict["3"] = copy.deepcopy(new_leaderboard_l_dict["2"])
            new_leaderboard_l_dict["2"] = copy.deepcopy(new_leaderboard_l_dict["1"])

            new_leaderboard_l_dict["1"]["count"].clear()
            new_leaderboard_l_dict["1"]["count"].append(el)
            new_leaderboard_l_dict["1"]["info"].clear()
            new_leaderboard_l_dict["1"]["info"]=el["info"]

        elif el["total"]>new_leaderboard_l_dict["2"]["count"][0]["total"]:

            new_leaderboard_l_dict["3"] = copy.deepcopy(new_leaderboard_l_dict["2"])

            new_leaderboard_l_dict["2"]["count"].clear()
            new_leaderboard_l_dict["2"]["count"].append(el)
            new_leaderboard_l_dict["2"]["info"].clear()
            new_leaderboard_l_dict["2"]["info"]=el["info"]

        elif el["total"]>new_leaderboard_l_dict["3"]["count"][0]["total"]:

            new_leaderboard_l_dict["3"]["count"].clear()
            new_leaderboard_l_dict["3"]["count"].append(el)
            new_leaderboard_l_dict["3"]["info"].clear()
            new_leaderboard_l_dict["3"]["info"]=el["info"]
    return new_leaderboard_l_dict

def gold(old_leaderboard_l_dict,encryptedEID,mongo):
    result_query = dict(mongo.get_full_from_eid(encryptedEID))
    array_gold_new=[]
    for el in dict(result_query["loots"]):
        gold_dict = dict({"1": 0, "2": 0, "3": 0, "total": 0,"info":{"stars":[0],"name":[""]}})
        for singol_drop in result_query["loots"][el]["drops"]:
            if singol_drop=="GOLD_METEORITE":
                gold_dict["info"]["stars"] = [result_query["loots"][el]["stars"]]
                gold_dict["info"]["name"] = [result_query["name"]]
                #TODO capacity
                for number in result_query["loots"][el]["drops"]["GOLD_METEORITE"]:
                    if number=="1":
                        gold_dict["1"]+=result_query["loots"][el]["drops"]["GOLD_METEORITE"]["1"]["COMMON"]["count"]
                    elif number=="2":
                        gold_dict["2"]+=result_query["loots"][el]["drops"]["GOLD_METEORITE"]["2"]["COMMON"]["count"]
                    elif number == "3":
                        gold_dict["3"] += result_query["loots"][el]["drops"]["GOLD_METEORITE"]["3"]["COMMON"]["count"]
        gold_dict["total"]=gold_dict["1"]+(gold_dict["2"]*9)+(gold_dict["3"]*9*11)
        array_gold_new.append(gold_dict)

    return check_and_update_file(old_leaderboard_l_dict,array_gold_new)


#TODO capacity to check if 2x
def update_leaderboard(old_leaderboard_dict,encryptedEID,mongo):
    old_leaderboard_dict["gold"]=(gold(old_leaderboard_dict["gold"],encryptedEID,mongo))
    return old_leaderboard_dict

