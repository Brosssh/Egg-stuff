from tabulate import tabulate

def __get_leader_arrays_ingr__(mongo,obj):
    header = ["Position", "Name", "Stars", "Capacity", "Tier 1", "Tier 2", "Tier 3","Total "+obj]
    table=[]
    leader_dict=mongo.get_leaderboard_stone_ingr()
    for i in range(1,len(leader_dict[obj])+1):
        this_list = []
        this_list.append(str(i))
        for sub_el in leader_dict[obj][str(i)]:
            for j in range(len(leader_dict[obj][str(i)]["name"])):
                if sub_el=="count":
                    for el in leader_dict[obj][str(i)][sub_el][j]:
                        this_list.append(str(j)+":"+str(leader_dict[obj][str(i)][sub_el][j][el]))

                if sub_el!="identifier" and sub_el!="count":
                    this_list.append(str(j)+":"+str(leader_dict[obj][str(i)][sub_el][j]))

        for i in range(0,int((len(this_list)-1)/7)):
            l=[this_list[0]]
            for el in this_list[1:]:
                ident,content=el.split(":")
                if str(ident)==str(i):
                    l.append(content)
            table.append(l)

    return table,header


def __get_leader_arrays_stone__(mongo,obj):
    header = ["Position", "Name", "Stars", "Capacity", "Tier 1", "Tier 2", "Tier 3", "Tier 4","Total "+obj]
    table=[]
    leader_dict=mongo.get_leaderboard_stone_ingr()
    for i in range(1,len(leader_dict[obj])+1):
        this_list = []
        this_list.append(str(i))
        for sub_el in leader_dict[obj][str(i)]:
            for j in range(len(leader_dict[obj][str(i)]["name"])):
                if sub_el=="count":
                    for el in leader_dict[obj][str(i)][sub_el][j]:
                        this_list.append(str(j)+":"+str(leader_dict[obj][str(i)][sub_el][j][el]))

                if sub_el!="identifier" and sub_el!="count":
                    this_list.append(str(j)+":"+str(leader_dict[obj][str(i)][sub_el][j]))

        for i in range(0,int((len(this_list)-1)/8)):
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

def tabulate_func(mongo,obj,ships_number=200,n=0):
    if obj=="gold" or obj=="titanium" or obj=="tau":
        table,header=__get_leader_arrays_ingr__(mongo,obj)
    else:
        table, header = __get_leader_arrays_stone__(mongo, obj)
    new_table=get_table_top_n(table,n)
    print(tabulate(new_table[:ships_number+1],headers=header, showindex="always"))

