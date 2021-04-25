from utils import utils
import itertools
import math
from os import sys, path
sys.path.append(path.dirname(__file__))




def sequence_to_vector_tag(sequence):
    vector = {}
    for nucleotide in sequence:
        if nucleotide in utils.specialNucleotidesRepresentations:
            for subNucleotide in utils.specialNucleotidesRepresentations[nucleotide]:
                try:
                    vector[subNucleotide] += 1/(len(utils.specialNucleotidesRepresentations[nucleotide]))
                except:
                    vector[subNucleotide] = 1/(len(utils.specialNucleotidesRepresentations[nucleotide]))
        else:
            try:
                vector[nucleotide] +=1
            except:
                vector[nucleotide] = 1
    print(vector)
    return vector

def sequence_to_vector_edge(sequence):
    edges = {}
    for i in range(len(sequence)-1):
        edge = sequence[i:i+2]
        if [ele for ele in utils.specialNucleotides if(ele in edge)]: #If edge contains complex nulceotide
            possibleNucleotidesFirstElement = edge[0]
            possibleNucleotidesSecondElement = edge[1]
            #Cheeck possible nucleotides of first and second element of edge
            if(edge[0] in utils.specialNucleotides):
                possibleNucleotidesFirstElement = utils.specialNucleotidesRepresentations[edge[0]]
            if (edge[1] in utils.specialNucleotides):
                possibleNucleotidesSecondElement = utils.specialNucleotidesRepresentations[edge[1]]

            #Get all combinations and distribute weight equally
            combinations = list(itertools.product(possibleNucleotidesFirstElement, possibleNucleotidesSecondElement))
            for combination in combinations:
                edge = ''.join(combination)
                try:
                    edges[edge] += 1/len(combinations)
                except:
                    edges[edge] = 1/len(combinations)

        else:
            try:
                edges[edge] += 1
            except:
                edges[edge] = 1

    print(edges)
    return edges

def sequence_to_vector_allpaths(sequence,maximumPathLength = 5):
    paths = {}
    for i in range(len(sequence)):
        for j in range(i,len(sequence)):
            if(maximumPathLength!=0 and j-i>=maximumPathLength):
                break
            path = sequence[i:j+1]


            if [ele for ele in utils.specialNucleotides if (ele in path)]:

                nucleotidesList = [nucleotide for nucleotide in path]

                fullListOfPossibleNucleotides = []

                #Each element in the list contains the possible nucleotides it can represent
                for nucleotide in nucleotidesList:
                    if (nucleotide in utils.specialNucleotides):
                        possibleNucleotides = utils.specialNucleotidesRepresentations[nucleotide]
                        fullListOfPossibleNucleotides.append(possibleNucleotides)
                    else:
                        fullListOfPossibleNucleotides.append([nucleotide])


                #Get all possible combinations
                combinations = list(itertools.product(*fullListOfPossibleNucleotides))

                for combination in combinations:
                    path = ''.join(combination)
                    try:
                        paths[path] += 1 / len(combinations)
                    except:
                        paths[path] = 1 / len(combinations)
            else:
                try:
                    paths[path] += 1
                except:
                    paths[path] = 1

    print(paths)
    return paths


def vector_cosine_measure(vector1,vector2):
    numerator = 0
    Asquared = 0
    Bsquared = 0

    #Matching the number of dimensions
    for key in list(vector1.keys()):
        try:
            element = vector2[key]
        except:
            vector2[key] = 0
    for key in list(vector2.keys()):
        try:
            element = vector1[key]
        except:
            vector1[key] = 0



   # print(vector1)
    #print(vector2)
    for key in list(vector2.keys()):
        numerator += (vector1[key] * vector2[key])
        Asquared += vector1[key] ** 2
        Bsquared += vector2[key] ** 2
    denominator = math.sqrt(Asquared * Bsquared)
    if denominator == 0:
       similarity = 0
    else:
        similarity = numerator / denominator
    #print(similarity)
    return similarity


def vector_pearsoncorrelation_measure(vector1,vector2):

    sumA = 0
    sumB = 0
    #Matching the number of dimensions
    for key in list(vector1.keys()):
        try:
            element = vector2[key]
            sumB += element
        except:
            vector2[key] = 0
    for key in list(vector2.keys()):
        try:
            element = vector1[key]
            sumA += element
        except:
            vector1[key] = 0

    averageA = sumA / len(vector1)
    averageB = sumB / len(vector2)

    numerator = 0
    denominator1 = 0
    denominator2 = 0
    #print('avg A: ',averageA)
    #print('avg B: ', averageB)
    for key in list(vector2.keys()):
        numerator += (vector1[key] - averageA) * (vector2[key] - averageB)
        denominator1 += (vector1[key] - averageA) ** 2
        denominator2 += (vector2[key] - averageB) ** 2


    denominator = math.sqrt(denominator1 * denominator2)

    if denominator == 0:
        #print('Denominator is 0')
        similarity = 1
    else:
        similarity = numerator / denominator
    #print(similarity)
    return similarity


def multiset_jackard_measure(set1,set2):
    # Matching the number of dimensions
    for key in list(set1.keys()):
        try:
            element = set2[key]
        except:
            vector2[key] = 0
    for key in list(set2.keys()):
        try:
            element = set1[key]
        except:
           set1[key] = 0

    numerator = 0
    sumA = 0
    sumB = 0
    for key in list(vector2.keys()):
        numerator += min(set1[key] , set2[key])
        sumA += set1[key]
        sumB += set2[key]

    denominator = sumA+sumB-numerator
    if denominator == 0:
        similarity = 0
    else:
        similarity = numerator / denominator
    # print(similarity)
    return similarity

def multiset_dice_measure(set1,set2):
    # Matching the number of dimensions
    for key in list(set1.keys()):
        try:
            element = set2[key]
        except:
            vector2[key] = 0
    for key in list(set2.keys()):
        try:
            element = set1[key]
        except:
           set1[key] = 0

    numerator = 0
    sumA = 0
    sumB = 0
    for key in list(vector2.keys()):
        numerator += min(set1[key] , set2[key])
        sumA += set1[key]
        sumB += set2[key]

    denominator = sumA+sumB
    if denominator == 0:
        similarity = 0
    else:
        similarity = (2*numerator) / denominator
    # print(similarity)
    return similarity








sequence3="ACAAGAUGCCAUUGUCCCCCGGCCUCCUGCUGCUGCUGCUCUCAAAGGCCACGGCCACCGCUGCSCUGCCCCUGGNGGGUGGCCCCACCGGCCGAGACARCGAGCAUACAGGAAGCGGGAGGAAUAAUGAVVAGCAGCCUGCAGUAACUUCUUCUGGAAGACCUUCUGCUCCUGCAAAUAAAACCUCACCCAUGAAUGCUCACGCAA"

import time

start = time.time()
#sequence_to_vector_allpaths(sequence3)
end = time.time()
print(end - start)



start = time.time()
#sequence_to_vector_edge(sequence3)
end = time.time()
print(end - start)


sequence1 = "NNNNN"
sequence2 = "AG"

vector1 = sequence_to_vector_allpaths(sequence1)
vector2 = sequence_to_vector_allpaths(sequence2)


similarity = vector_cosine_measure(vector1,vector2)

print('Cosine: ',similarity)

similarity2  = vector_pearsoncorrelation_measure(vector1,vector2)

print('Pearson: ',similarity2)

similarity3  = multiset_jackard_measure(vector1,vector2)

print('Jackard: ',similarity3)

similarity4  = multiset_dice_measure(vector1,vector2)

print('Dice: ',similarity4)