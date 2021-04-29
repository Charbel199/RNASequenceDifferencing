
specialNucleotides = ['R', 'M', 'S', 'V', 'N']
specialNucleotidesRepresentations = {
    'R': ['G', 'A'],
    'M': ['A', 'C'],
    'S': ['G', 'C'],
    'V': ['G', 'A', 'C'],
    'N': ['G', 'U', 'A', 'C']
}


allPossibleNucleotides = ['R', 'M', 'S', 'V', 'N', 'G', 'U', 'A', 'C']

# Util intersection method
def intersection(lst1, lst2):
    return list(set(lst1) & set(lst2))


# Util union method
def union(lst1, lst2):
    return lst1 + list(set(lst2) - set(lst1))
