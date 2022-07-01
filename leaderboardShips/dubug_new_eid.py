from leaderboardShips.ships_functions import *
from utiliy import encrypt_string

def force_leader_update(mongo):
    ids=mongo.get_all_encrypted_IDs()
    for el in ids:
        new_ships=mongo.get_full_from_eid(el["EID"])

        leaderboard_dict = mongo.build_full_leaderboard()
        leaderboard_updated = update_leaderboard(leaderboard_dict, new_ships)
        for el in leaderboard_updated:
            mongo.load_updated_document_by_name(leaderboard_updated[el], el)

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

        leaderboard_dict=mongo.build_full_leaderboard()
        leaderboard_updated = update_leaderboard(leaderboard_dict, new_ships)
        for el in leaderboard_updated:
            mongo.load_updated_document_by_name(leaderboard_updated[el],el)

        print("OK")

