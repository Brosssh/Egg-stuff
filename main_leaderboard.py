from new_EID import insert_EID
from mongoDB_manager import mongo_manager

conn = None

mongo = mongo_manager(conn)

insert_EID(mongo)

