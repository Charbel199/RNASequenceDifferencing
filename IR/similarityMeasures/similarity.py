from utils import utils
import itertools
import math
import time
import numpy as np
from similarityMeasures import updateLogic
##TED
def TEDSimilarity_measure(sourceArr, destinationArr, medicalSimilarity=0):
    # Initializing empty distance array
    distArr = np.empty(shape=(len(sourceArr) + 1, len(destinationArr) + 1), dtype=np.float16)

    # Source index represent the row's index and destination index represent the column's index
    for sourceIndex in range(distArr.shape[0]):
        for destinationIndex in range(distArr.shape[1]):

            # Initialize first row
            if sourceIndex == 0:
                if destinationIndex == 0:
                    distArr[sourceIndex, destinationIndex] = 0
                else:
                    distArr[sourceIndex, destinationIndex] = distArr[sourceIndex, destinationIndex - 1] + 1
                continue
            # Initialize first column
            elif destinationIndex == 0:
                distArr[sourceIndex, destinationIndex] = distArr[sourceIndex - 1, destinationIndex] + 1
                continue

            # Value in left cell
            prevInsert = distArr[sourceIndex, destinationIndex - 1]
            # Value in top cell
            prevDelete = distArr[sourceIndex - 1, destinationIndex]
            # Value in top-left diagonal cell
            prevUpdate = distArr[sourceIndex - 1, destinationIndex - 1]

            # Insert and delete cost 1
            # Calculating the update cost:
            if sourceArr[sourceIndex - 1] != destinationArr[destinationIndex - 1]:
                # Source and destination nucleotide loaded
                sourceNode = str(sourceArr[sourceIndex - 1])
                destinationNode = str(destinationArr[destinationIndex - 1])
                # Get update value
                updateValue = updateLogic.updateNode(sourceNode, destinationNode, medicalSimilarity=medicalSimilarity)
            else:
                # If same nucleotide cost = 0
                updateValue = 0
            # Get minimum cost
            minimumCost = min([prevInsert + 1, prevDelete + 1, prevUpdate + updateValue])
            # Set minimum cost
            distArr[sourceIndex, destinationIndex] = minimumCost

    editdistance = distArr[distArr.shape[0] - 1][distArr.shape[1] - 1]
    if len(sourceArr) + len(destinationArr) != 0:
        similarity = 1 - editdistance / (len(sourceArr) + len(destinationArr))
    else:
        similarity = 1
    return similarity


##Vector based
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

##Set based
def multiset_jackard_measure(set1,set2):
    # Matching the number of dimensions
    for key in list(set1.keys()):
        try:
            element = set2[key]
        except:
            set2[key] = 0
    for key in list(set2.keys()):
        try:
            element = set1[key]
        except:
           set1[key] = 0

    numerator = 0
    sumA = 0
    sumB = 0
    for key in list(set1.keys()):
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
            set2[key] = 0
    for key in list(set2.keys()):
        try:
            element = set1[key]
        except:
           set1[key] = 0

    numerator = 0
    sumA = 0
    sumB = 0
    for key in list(set2.keys()):
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



def compute_all_similarities(sourceArr,destinationArr,tokenizationMethod):
    elements1 = tokenizationMethod(sourceArr)
    elements2 = tokenizationMethod(destinationArr)

    similarities = []
    times = []

    start = time.time()
    similarity = TEDSimilarity_measure(sourceArr,destinationArr)
    end = time.time()
    similarities.append(similarity)
    times.append(end - start)

    start = time.time()
    similarity = vector_cosine_measure(elements1,elements2)
    end = time.time()
    similarities.append(similarity)
    times.append(end - start)

    start = time.time()
    similarity = vector_pearsoncorrelation_measure(elements1,elements2)
    end = time.time()
    if(similarity<-0.99):
        similarity=-1
    similarities.append(similarity)
    times.append(end - start)

    start = time.time()
    similarity = multiset_jackard_measure(elements1, elements2)
    end = time.time()
    similarities.append(similarity)
    times.append(end - start)

    start = time.time()
    similarity = multiset_dice_measure(elements1, elements2)
    end = time.time()
    similarities.append(similarity)
    times.append(end - start)


    return similarities,times