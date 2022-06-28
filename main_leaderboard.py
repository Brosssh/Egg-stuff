from leaderboardShips.new_EID import insert_EID
from leaderboardShips.dubug_new_eid import insert_EID_dubug
from leaderboardShips.mongoDB_manager import mongo_manager
from leaderboardShips.show_leaderboard import *

print("This is a very test")

#lines = open("D:/mongo_cred.txt", "r").read().split('\n')
#user = lines[0]
#pssw = lines[1]

#conn = "mongodb+srv://" + user + ":" + pssw + "@eggcluster.sbrsi.mongodb.net/?retryWrites=true&w=majority"

conn="mongodb+srv://Ro0t:yfPVFbCPWhs7rCvW@eggcluster.sbrsi.mongodb.net/?retryWrites=true&w=majority"
mongo = mongo_manager(conn)

valid=False
while not valid:
    choice=str(input("Press 1 if you want to submit your EID, 2 to see the leaderboard: "))
    if choice=="1":
        insert_EID(mongo)
        #insert_EID_dubug(mongo)
    elif choice=="2":
        valid_ships_number=False
        while not valid_ships_number:
            try:
                ships_number = int(input("How many ships do you want to display? "))
                if ships_number>0:
                    tabulate_func(mongo,ships_number)
                else:
                    print("Only a positive number is accepted\n")
            except:
                print("Only a positive number is accepted\n")
    else:
        print("Only 1 or 2 ")
