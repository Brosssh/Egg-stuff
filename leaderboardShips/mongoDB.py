#MONGO IS NOT THE OPTIMAL CHOICE, IK, BUT IT'S FREE SO I'LL USE IT
from pymongo import MongoClient

class mongo_manager:

    client=None

    def __init__(self,conn_string):
        try:
            self.client = MongoClient(conn_string)
        except:
            print("Something went wrong with the database connection")



    def __get_collection__(self):
        try:
            mydb = self.client["db_leaderboard"]
            mycol = mydb["users_ship"]
            return mycol
        except:
            print("Something went wrong with the database connection")


    def insert_full_user_ships(self,dict_to_insert):
        try:
            self.__get_collection__().insert_one(dict_to_insert)
        except Exception as e:
            print(e)

    def get_drop_by_name(self,name):
        path="ships.ship.drops."+name
        return self.__get_collection__().find({path:{"$exists":1}})


    def get_full_from_eid(self,eid):
        try:
            return self.__get_collection__().find_one({'EID':eid})
        except Exception as e:
            print(e)

    def user_exists(self, encryptedEID):
        try:
            res= self.__get_collection__().find_one({'EID':encryptedEID})
            if res is None:
                return False
            else:
                return True
        except Exception as e:
            print(e)

    def update_and_return_user_ships(self, final_dict, encryptedEID):
        ships=self.__get_collection__().find({"EID":encryptedEID},{"ships":1})
        list_already_stored=[]
        for el in ships:
            for i in range(len(el["ships"])):
                list_already_stored.append(el["ships"][i]["identifier"])

        to_append=[]
        for el in final_dict["ships"]:
            if el["identifier"] not in list_already_stored:
                to_append.append(el)
        if len(to_append) > 0:
            print("Inserting "+str(len(to_append))+" new ships to the database")
            #get old doc
            doc=self.get_full_from_eid(encryptedEID)
            for el in to_append:
                doc["ships"].append(el)
            self.__get_collection__().delete_one({"EID":encryptedEID})
            self.__get_collection__().insert_one(doc)
            return doc
        else:
            print("No new ships")


