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
      #  if c>=3:
#            break
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
    new_dict=[]
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

def check_if_same_total(leaderboard,current_el,n_pos):
    for pos in [str(el) for el in range(1,n_pos+1)]:
        if leaderboard[pos]["count"][0]["total"] == current_el["count"]["total"]:
            for sub_el in current_el:
                leaderboard[pos][sub_el].append(current_el[sub_el])
    return leaderboard


def move_all_down(start,stop,current_el,leaderboard):
    for i in range(int(stop),int(start),-1):
        leaderboard[str(i)]=copy.deepcopy(leaderboard[str(i-1)])
    for sub_el in current_el:
        leaderboard[start][sub_el].clear()
        leaderboard[start][sub_el].append(copy.deepcopy(current_el[sub_el]))
    return leaderboard


def check_if_beetween_total(leaderboard,current_el,n_pos):
    for pos in [str(el) for el in range(1, n_pos + 1)]:
        if current_el["count"]["total"]>leaderboard[pos]["count"][0]["total"]:
            move_all_down(pos,n_pos,current_el,leaderboard)
        return leaderboard


#this code below is shit, need to be fixed
def check_and_update_file(old_leadberboard_l_dict,array_new_gold,n_pos):
    new_leaderboard_l_dict=old_leadberboard_l_dict
    array_new_gold=sorted(array_new_gold, key = lambda item: item['count']['total'])
    for el in array_new_gold[-n_pos:]:
        new_leaderboard_l_dict=check_if_same_total(new_leaderboard_l_dict,el,n_pos)
        new_leaderboard_l_dict=check_if_beetween_total(new_leaderboard_l_dict,el,n_pos)
    return new_leaderboard_l_dict

def gold(old_leaderboard_l_dict,new_ships,n_pos):
    array_gold_new=[]
    user=new_ships["name"]
    for el in new_ships["ships"]:
        gold_dict = dict({"count":{"1": 0, "2": 0, "3": 0, "total": 0},"stars":0,"name":"","capacity": 0})
        for singol_drop in el["drops"]:
            if singol_drop=="GOLD_METEORITE":
                gold_dict["stars"] = el["stars"]
                gold_dict["name"] = user
                gold_dict["capacity"] = el["capacity"]
                gold_dict["identifier"] = el["identifier"]
                for number in el["drops"]["GOLD_METEORITE"]:
                    gold_dict["count"][number]+=el["drops"]["GOLD_METEORITE"][number]["COMMON"]["count"]
        gold_dict["count"]["total"]=gold_dict["count"]["1"]+(gold_dict["count"]["2"]*9)+(gold_dict["count"]["3"]*9*11)
        array_gold_new.append(gold_dict)

    return check_and_update_file(old_leaderboard_l_dict,array_gold_new,n_pos)


def update_leaderboard(old_leaderboard_dict,new_ships,n_pos):
    old_leaderboard_dict["gold"]=(gold(old_leaderboard_dict["gold"],new_ships,n_pos))
    return old_leaderboard_dict

