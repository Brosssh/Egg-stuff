from leaderboardShips.new_EID import insert_EID
from leaderboardShips.mongoDB_manager import mongo_manager
from leaderboardShips.show_leaderboard import show_leader

print("This is a very test")

lines = open("D:/mongo_cred.txt", "r").read().split('\n')
user = lines[0]
pssw = lines[1]

conn = "mongodb+srv://" + user + ":" + pssw + "@eggcluster.sbrsi.mongodb.net/?retryWrites=true&w=majority"
mongo = mongo_manager(conn)

try:
    choice=str(input("Press 1 if you want to submit your EID, 2 to see the leaderboard: "))
    if choice=="1":
        insert_EID(mongo)
    elif choice=="2":
        show_leader(mongo)
    else:
        print("Only 1 or 2 ")
except:
    print("Only 1 or 2 ")