from leaderboardShips.ships_functions import *
from server_manager import server

''''
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

loot=loots(result,server_manager)
'''
with open('C:\\Users\\tiabr\\Desktop\\ship_json.txt') as loot_json:
    loot_dict = json.load(loot_json)
    semplify_dict(loot_dict)
