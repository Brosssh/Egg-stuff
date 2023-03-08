import threading

import utility
from ships_functions import *
from server_manager import server
from utility import encrypt_string
import os


def insert_EID(mongo):
    checksum = 0

    while checksum == 0:
        try:
            EID = str(input("Please enter your EID: "))
            server_manager = server()
            server_manager.set_EID(EID)
            result = server_manager.execute_call()
            checksum = result.backup.checksum
            if checksum == 0:
                print("EID not registered on Egg Inc server\n")
            else:
                break
        except:
            print("Insert valid EID (EI12345678)\n")

    encryptedEID = encrypt_string(EID)

    loot_dict = loots(result, server_manager, mongo, encryptedEID)

    user_name = result.backup.user_name

    dict_loots = semplify_dict(loot_dict)

    final_dict = {"EID": encryptedEID, "name": user_name, "ships": dict_loots}

    #ships that weren't on the db before this execution, will be modified below
    new_ships = final_dict

    if not mongo.user_exists(encryptedEID):
        mongo.insert_full_user_ships(final_dict)
        print("Data successfully loaded!")
    else:
        new_ships = mongo.update_and_return_user_ships(final_dict,
                                                       encryptedEID)
        if new_ships is not None:
            print("Data successfully updated!")
        else:
            print("Your ships are already up to date")

    if new_ships is not None:
        print("\nUpdating the leaderboard with your ships \n")
        leaderboard_dict = mongo.build_full_leaderboard()
        leaderboard_updated = update_leaderboard(leaderboard_dict, new_ships)
        for el in tqdm(leaderboard_updated):
            mongo.load_updated_document_by_name(leaderboard_updated[el], el)
        print("\nThanks for your submission :)\n")
