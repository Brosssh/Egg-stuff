from leaderboardShips.new_EID import insert_EID
from leaderboardShips.mongoDB_manager import mongo_manager
from leaderboardShips.show_leaderboard import *
from utiliy import ask_and_wait_valid_answer, ask_and_wait_pos_integer

lines = open("D:/mongo_cred.txt", "r").read().split('\n')
user = lines[0]
pssw = lines[1]

conn = "mongodb+srv://" + user + ":" + pssw + "@eggcluster.sbrsi.mongodb.net/?retryWrites=true&w=majority"

stones_array = ["CLARITY_STONE", "LUNAR_STONE", "PROPHECY_STONE", "LIFE_STONE", "QUANTUM_STONE", "DILITHIUM_STONE",
                "SOUL_STONE", "TERRA_STONE", "TACHYON_STONE", "SHELL_STONE"]

arti_array = ["LIGHT_OF_EGGENDIL", "BOOK_OF_BASAN", "TACHYON_DEFLECTOR", "SHIP_IN_A_BOTTLE", "TITANIUM_ACTUATOR",
              "DILITHIUM_MONOCLE", "QUANTUM_METRONOME", "PHOENIX_FEATHER", "THE_CHALICE", "INTERSTELLAR_COMPASS",
              "CARVED_RAINSTICK", "BEAK_OF_MIDAS", "MERCURYS_LENS", "NEODYMIUM_MEDALLION", "ORNATE_GUSSET",
              "TUNGSTEN_ANKH", "AURELIAN_BROOCH", "VIAL_MARTIAN_DUST", "DEMETERS_NECKLACE", "LUNAR_TOTEM", "PUZZLE_CUBE"]

mongo = mongo_manager(conn)



while True:
    choice=0
    while choice==0:
        try:
            choice=ask_and_wait_valid_answer(["1","2"],"Press 1 if you want to submit your EID, 2 to see the leaderboard: ")
            if choice=="1":
                insert_EID(mongo)
            elif choice=="2":
                inp=ask_and_wait_valid_answer(mongo.get_leaderboards_names(),"Enter the item you want to show the leaderboard for (check this Replit description for the list of possible input): ")
                top_n=ask_and_wait_pos_integer("How many ships do you want to display? ")
                top_n_person=ask_and_wait_pos_integer("How many ships per person do you want to display? (Top n for the total, enter 0 if you want to display all of them): ")
                tabulate_func(mongo, inp, top_n, top_n_person)
        except Exception as e:
            print(e)