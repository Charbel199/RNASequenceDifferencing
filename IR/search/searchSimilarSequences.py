from IR_METHODS.similarityMeasures import similarity
import time
from IR_METHODS.TFIDF import TFIDF
def IR_Method(sequencesDatabase,inputSequence,result,times,tokenizationMethod,similarityMethod,TF_method,IDF_method,preprocessed = 0,processed_sequences_database = [],numberOfOutputs = 3,numberOfSequencesToSearch = 100,TF = 1,IDF = 0, epsilon=2, operator='KNN' ):
    # If 0 sequences to search, search in the entire db
    if(numberOfSequencesToSearch == 0):
        numberOfSequencesToSearch = len(sequencesDatabase)

    # If ED of project 1
    if(similarityMethod == similarity.TEDSimilarity_measure ):
        similarities = {}
        sequencesDatabase = sequencesDatabase[0:numberOfSequencesToSearch]
        start = time.time()



        for i, sequence in enumerate(sequencesDatabase):
            sim = similarityMethod(inputSequence, sequence)
            similarities[sequencesDatabase[i]] = sim

        end = time.time()

    # If multiset / vector
    else:
        sequencesDatabase = sequencesDatabase[0:numberOfSequencesToSearch]
        start = time.time()
        # If NOT preprocessed
        if(len(processed_sequences_database) == 0):
            print("PREPROCESSING")
            processed_sequences_database = list(map(tokenizationMethod, sequencesDatabase))

            processed = []
            for elements in processed_sequences_database:
                processed.append(TFIDF.updateWeights(elements,processed_sequences_database,TF_method,IDF_method,TF = TF,IDF = IDF))
            processed_sequences_database = processed
        # If NOT complete preprocessed
        if(len(processed_sequences_database) != len(sequencesDatabase)):
            print("PREPROCESSING")
            processed_sequences_database = list(map(tokenizationMethod, sequencesDatabase))
            processed = []
            for elements in processed_sequences_database:
                processed.append(
                    TFIDF.updateWeights(elements, processed_sequences_database, TF_method, IDF_method, TF=TF,
                                               IDF=IDF))
            processed_sequences_database = processed



        similarities = {}
        # TAG BASED or EDGE BASED or ALL PATH BASED
        processedInputSequence = tokenizationMethod(inputSequence)
        for i,sequence in enumerate(processed_sequences_database):
            # Dice or Jaccard or Cosine or Pearson Correlation
            sim = similarityMethod(processedInputSequence, sequence)
            similarities[sequencesDatabase[i]] = sim
        end = time.time()




    from collections import Counter
    cnt = Counter(similarities)

    # Finding values within range epsilon
    withinRange = cnt.most_common(len(cnt))
    rangeDict = {}
    for w in withinRange:
        if (1/w[1]) < epsilon:
            rangeDict[w[0]] = w[1]

    # Finding k highest values
    high = cnt.most_common(numberOfOutputs)
    highDict = {}
    for h in high:
        highDict[h[0]]=h[1]
    from operator import itemgetter

    # Finding k lowest values
    low = dict(sorted(similarities.items(), key=itemgetter(1))[:numberOfOutputs])

    # Finding combined range and KNN operator:
    combinedDict = dict(list(rangeDict.items())[:numberOfOutputs])
    print(combinedDict)

    if(operator=='KNN'):
        result.append(highDict)
        result.append(low)
        print(result)
    elif(operator=='Range'):
        result.append(rangeDict)
    else:
        result.append(combinedDict)
        print(result)
    times.append(end - start)
    return result
