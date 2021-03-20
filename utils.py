#Util intersection method
def intersection(lst1, lst2):
    return list(set(lst1) & set(lst2))
#Util union method
def union(lst1, lst2):
    return lst1 + list(set(lst2) - set(lst1))
