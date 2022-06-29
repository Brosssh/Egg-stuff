from leaderboardShips.new_EID import insert_EID
from leaderboardShips.mongoDB_manager import mongo_manager
from leaderboardShips.show_leaderboard import *

lines = open("D:/mongo_cred.txt", "r").read().split('\n')
user = lines[0]
pssw = lines[1]

conn = "mongodb+srv://" + user + ":" + pssw + "@eggcluster.sbrsi.mongodb.net/?retryWrites=true&w=majority"

mongo = mongo_manager(conn)

valid=False
while not valid:
    choice=str(input("Press 1 if you want to submit your EID, 2 to see the leaderboard: "))
    if choice=="1":
        insert_EID(mongo)
    elif choice=="2":
        ing_input_valid=False
        valid_ships_number = False
        while not ing_input_valid:
            ing_input=str(input("Enter G to dislay gold meteorite, C for tau ceti and T for titanium: "))
            if ing_input=="G" or ing_input=="C" or ing_input=="T":
                ingredient_choice="gold" if ing_input =="G" else "tau" if ing_input =="C" else "titanium" if ing_input =="T" else None
                while not valid_ships_number:
                    try:
                        ships_number = int(input("How many ships do you want to display? "))
                        if ships_number>0:
                            valid_n_number = False
                            while not valid_n_number:
                                try:
                                    n_number = int(input("How many ships per person do you want to display? (Top n total gold, enter 0 if you want to display all of them)...  "))
                                    if n_number >= 0:
                                        tabulate_func(mongo,ingredient_choice,ships_number, n_number)
                                        valid_ships_number=True
                                        break
                                    else:
                                        print("Only a positive number or 0 is accepted\n")
                                except:
                                    print("Only a positive number or 0 is accepted\n")
                        else:
                            print("Only a positive number is accepted\n")
                    except:
                        print("Only a positive number is accepted\n")
                break
            else:
                print("Only a G, C or T\n")
    else:
        print("Only 1 or 2 ")
