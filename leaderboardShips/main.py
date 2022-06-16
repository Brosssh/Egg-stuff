from leaderboardShips.ships_functions import *
from server_manager import server
from mongoDB import mongo_manager
from utiliy import encrypt_string

checksum=0

while checksum==0:
    try:
        EID = str(input("Please enter your EID (it won't be steal/saved anywhere): "))
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

final_dict={"EID":encryptedEID,"name":user_name,"loots":dict_loots}

'''

with open('D:\\ship_json.txt') as loot_json:
    loot_dict = json.load(loot_json)
    loots=semplify_dict(loot_dict)

final_dict={"EID":"test_eid","name":"Q","loots":loots}
'''

lines = open("D:/mongo_cred.txt", "r").read().split('\n')
user=lines[0]
pssw=lines[1]

mongo_manager=mongo_manager(user,pssw)
mongo_manager.insert_full_user_ships(final_dict)

