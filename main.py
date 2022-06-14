from LLC import *
from server_manager import server

lines = open("C:/eid.txt", "r").read().split('\n')

EID=lines[0]

server_manager=server()
server_manager.set_EID(EID)

result=server_manager.execute_call()

#print(server_manager.get_loot("agxhdXhicmFpbmhvbWVyFgsSCUVJTWlzc2lvbhiAgJCB1rm6Cww"))

#print(get_array_ships_ID(result))

print("Total legendaries: "+str(get_leg_number_total(result)))

print("\nTotal drops from exthens: "+ str(get_total_drop_exthens(result)))

print("\nTotal craftings (with legendary possibility):" + str(get_total_craft(result)))

print("\nTotal extended henerprise: "+str(get_total_ships_exthens(result)))
print("Total standard henerprise: "+str(get_total_ships_standhens(result)))
print("Total short henerprise: "+str(get_total_ships_shens(result)))

print("\nLLC: "+str(formula_LLC(get_leg_number_total(result),get_total_craft(result),get_total_ships_exthens(result),get_total_ships_standhens(result),get_total_ships_shens(result))))