from utils import utils
import math
from os import sys, path
sys.path.append(path.dirname(__file__))




def sequence_to_vector_tag(sequence):
    vector = {}
    for nucleotide in sequence:
        try:
            vector[nucleotide] +=1
        except:
            vector[nucleotide] = 1
   # print(vector)
    return vector

def sequence_to_vector_edge(sequence):
    edges = {}
    for i in range(len(sequence)-1):
        try:
            edges[sequence[i:i+2]] += 1
        except:
            edges[sequence[i:i+2]] = 1

    #print(edges)
    return edges

def sequence_to_vector_allpaths(sequence,maximumPathLength = 5):
    paths = {}
    for i in range(len(sequence)):
        for j in range(i,len(sequence)):
            if(maximumPathLength!=0 and j-i>=maximumPathLength):
                break
            try:
                paths[sequence[i:j+1]] += 1
            except:
                paths[sequence[i:j+1]] = 1

   # print(paths)
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



    print(vector1)
    print(vector2)
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
    print('avg A: ',averageA)
    print('avg B: ', averageB)
    for key in list(vector2.keys()):
        numerator += (vector1[key] - averageA) * (vector2[key] - averageB)
        denominator1 += (vector1[key] - averageA) ** 2
        denominator2 += (vector2[key] - averageB) ** 2


    denominator = math.sqrt(denominator1 * denominator2)

    if denominator == 0:
        print('Denominator is 0')
        similarity = 1
    else:
        similarity = numerator / denominator
    #print(similarity)
    return similarity





sequence3="ACAAGAUGCCAUUGUCCCCCGGCCUCCUGCUGCUGCUGCUCUCAAAGGCCACGGCCACCGCUGCSCUGCCCCUGGNGGGUGGCCCCACCGGCCGAGACARCGAGCAUACAGGAAGCGGGAGGAAUAAUGAVVAGCAGCCUGCAGUAACUUCUUCUGGAAGACCUUCUGCUCCUGCAAAUAAAACCUCACCCAUGAAUGCUCACGCAA"

import time

start = time.time()
sequence_to_vector_allpaths(sequence3)
end = time.time()
print(end - start)



start = time.time()
sequence_to_vector_edge(sequence3)
end = time.time()
print(end - start)


sequence1 = "A"
sequence2 = "AA"

vector1 = sequence_to_vector_allpaths(sequence1)
vector2 = sequence_to_vector_allpaths(sequence2)


similarity = vector_cosine_measure(vector1,vector2)

print('Similarity: ',similarity)

similarity2  = vector_pearsoncorrelation_measure(vector1,vector2)

print('Similarity2: ',similarity2)