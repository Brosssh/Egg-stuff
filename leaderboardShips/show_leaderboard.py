from tabulate import tabulate

def show_leader(mongo):
    table=[]
    leader_dict=mongo.get_leaderboard()
    for i in range(1,len(leader_dict["gold"])+1):
        this_list = []
        this_list.append(str(i))
        for sub_el in leader_dict["gold"][str(i)]:
            for j in range(len(leader_dict["gold"][str(i)]["name"])):
                if sub_el!="identifier":
                    this_list.append(str(leader_dict["gold"][str(i)][sub_el][j]))
                if sub_el=="count":
                    for el in leader_dict["gold"][str(i)][sub_el][j]:
                        if el!="total":
                            this_list.append(leader_dict["gold"][str(i)][sub_el][j][el])
        table.append(this_list)
    print(tabulate(table,headers=["Position","Name","Stars","Capacity","Tier 1","Tier 2","Tier 3"]))

