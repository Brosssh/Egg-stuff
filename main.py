from LLC import *
from server_manager import server

#lines = open("C:/eid.txt", "r").read().split('\n')
#EID=lines[1]

checksum=0

while checksum==0:
    try:
        EID = str(input("Please enter your EID (it won't be steal/saved anywhere): "))
        server_manager = server()
        server_manager.set_EID(EID)
        result = server_manager.execute_call()
        checksum=result.backup.checksum
        if checksum==0:
            print("EID not registered on Egg Inc server\n")
        else:
            break
    except:
        print("Insert valid EID (EI12345678)\n")

#print("Total legendaries: "+str(get_leg_number_total(result)))
print("\nHello "+result.backup.user_name+", glad to see you here")

print("\nTotal drops from exthens: "+ str(get_total_drop_exthens(result)))

print("\nTotal craftings (with legendary possibility):" + str(get_total_craft(result)))

print("\nTotal extended henerprise: "+str(get_total_ships_exthens(result)))
print("Total standard henerprise: "+str(get_total_ships_standhens(result)))
print("Total short henerprise: "+str(get_total_ships_shens(result)))

print("\nCredit to EffectiveMess#0256 for the formula\n")
print("\nLLC: "+str(formula_LLC(get_leg_number_total(result),get_total_craft(result),get_total_ships_exthens(result),get_total_ships_standhens(result),get_total_ships_shens(result))))

print("\nHave a good day (:")