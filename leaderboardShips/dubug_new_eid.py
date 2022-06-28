from leaderboardShips.ships_functions import *
from server_manager import server
from utiliy import encrypt_string
import os


def insert_EID_dubug(mongo):

    with open('D:\\ship_json.txt') as loot_json:
        loot_dict = json.load(loot_json)
        loots=semplify_dict(loot_dict)

    encryptedEID = encrypt_string("test_eid")
    final_dict={"EID":encryptedEID,"name":"Q","ships":loots}

    # ships that weren't on the db before this execution, will be modified below
    new_ships = final_dict

    if not mongo.user_exists(encryptedEID):
        #mongo.insert_full_user_ships(final_dict)
        print("Data successfully loaded!")
    else:
        new_ships = mongo.update_and_return_user_ships(final_dict, encryptedEID)
        if new_ships is not None:
            print("Data successfully updated!")
        else:
            print("No new ships")

    if new_ships is not None:
        leaderboard_dict = mongo.get_leaderboard()

        leaderboard_updated = update_leaderboard(leaderboard_dict, new_ships)
        mongo.load_updated_leaderboard(leaderboard_updated)

