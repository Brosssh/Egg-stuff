from leaderboardShips.ships_functions import *
from server_manager import server
from mongoDB import mongo_manager
from utiliy import encrypt_string
import os

checksum=0

while checksum==0:
    try:
        EID = str(input("Please enter your EID (only your in-game name (and ship loots) will be stored, the EID will be encrypted, so unreadable to me): "))
        server_manager = server()
        server_manager.set_EID(EID)
        result = server_manager.execute_call()
        checksum=result.backup.checksum
        if checksum==0:
            print("EID not registered on Egg Inc server\n")
        else:
            break
    except:
        print("Insert valid EID (EI12345678)\n")

loot_dict=loots(result,server_manager)

user_name=result.backup.user_name

dict_loots=semplify_dict(loot_dict)

encryptedEID = encrypt_string(EID)

final_dict={"EID":encryptedEID,"name":user_name,"ships":dict_loots}

#conn=os.getenv("mongo_conn")

'''

with open('D:\\ship_json.txt') as loot_json:
    loot_dict = json.load(loot_json)
    loots=semplify_dict(loot_dict)

encryptedEID = encrypt_string("test_eid")
final_dict={"EID":encryptedEID,"name":"Q","loots":loots}

'''
lines = open("D:/mongo_cred.txt", "r").read().split('\n')
user=lines[0]
pssw=lines[1]

conn="mongodb+srv://"+user+":"+pssw+"@eggcluster.sbrsi.mongodb.net/?retryWrites=true&w=majority"

#ships that weren't on the db before this execution, will be modified below
new_ships=final_dict

mongo=mongo_manager(conn)
if not mongo.user_exists(encryptedEID):
    #mongo.insert_full_user_ships(final_dict)
    print("Data successfully loaded!")
else:
    #new_ships=mongo.update_and_return_user_ships(final_dict,encryptedEID)
    print("Data successfully updated!")




with open('leaderboard.json') as old_leaderboard:
    leaderboard_dict = json.load(old_leaderboard)

leaderboard_updated=update_leaderboard(leaderboard_dict,new_ships)
print(leaderboard_updated)
#TODO caricamento file su mongo