from utils import utils
import itertools
import math



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
    #print(vector)
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

    #print(edges)
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

   # print(paths)
    return paths
