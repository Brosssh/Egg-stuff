#MONGO IS NOT THE OPTIMAL CHOICE, IK, BUT IT'S FREE SO I'LL USE IT
from pymongo import MongoClient

class mongo_manager:

    conn_string="unset"
    client=None

    def __init__(self,user,pssw):
        try:
            self.conn_string="mongodb+srv://"+user+":"+pssw+"@eggcluster.sbrsi.mongodb.net/?retryWrites=true&w=majority"
            self.client = MongoClient(self.conn_string)
        except:
            print("Something went wrong with the database connnection")

    def __get_collection__(self):
        try:
            mydb = self.client["db_leaderboard"]
            mycol = mydb["users_ship"]
            return mycol
        except:
            print("Something went wrong with the database connnection")

    def insert_full_user_ships(self,dict_to_insert):
        try:
            self.__get_collection__().insert_one(dict_to_insert)
        except:
            print("Something went wrong with the database connnection")
