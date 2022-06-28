from tabulate import tabulate

def __get_leader_arrays__(mongo):
    header = ["Position", "Name", "Stars", "Capacity", "Tier 1", "Tier 2", "Tier 3","Total gold"]
    table=[]
    leader_dict=mongo.get_leaderboard()
    for i in range(1,len(leader_dict["gold"])+1):
        this_list = []
        this_list.append(str(i))
        for sub_el in leader_dict["gold"][str(i)]:
            for j in range(len(leader_dict["gold"][str(i)]["name"])):
                if sub_el=="count":
                    for el in leader_dict["gold"][str(i)][sub_el][j]:
                        this_list.append(str(j)+":"+str(leader_dict["gold"][str(i)][sub_el][j][el]))

                if sub_el!="identifier" and sub_el!="count":
                    this_list.append(str(j)+":"+str(leader_dict["gold"][str(i)][sub_el][j]))

        for i in range(0,int((len(this_list)-1)/7)):
            l=[this_list[0]]
            for el in this_list[1:]:
                ident,content=el.split(":")
                if str(ident)==str(i):
                    l.append(content)
            table.append(l)

    return table,header

#top n ships for users
def get_table_top_n(table,n):
    if n==0:
        return table
    users={}
    new_table=[]
    for el in table:
        if el[1] in users.keys():
            if users[el[1]]<n:
                users[el[1]]+=1
                new_table.append(el)
        else:
            users[el[1]]=1
            new_table.append(el)
    return new_table

def tabulate_func(mongo,ships_number=200,n=0):
    table,header=__get_leader_arrays__(mongo)
    new_table=get_table_top_n(table,n)
    print(tabulate(new_table[:ships_number],headers=header))

