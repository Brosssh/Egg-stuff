from LLC import *
from server_manager import server

EID = open("C:/eid.txt", "r").read()


server_manager=server()
server_manager.set_EID(EID)

result=server_manager.execute_call()

print(server_manager.get_loot("agxhdXhicmFpbmhvbWVyFgsSCUVJTWlzc2lvbhiAgJCB1rm6Cww"))

print(get_array_ships_ID(result))

print(get_leg_number_ships(result,server_manager))
