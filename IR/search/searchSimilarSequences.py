from similarityMeasures import similarity
import time
from search import TFIDF
def IR_Method(sequencesDatabase,inputSequence,result,times,tokenizationMethod,similarityMethod,TF_method,IDF_method,preprocessed = 0,processed_sequences_database = [],numberOfOutputs = 3,numberOfSequencesToSearch = 100,TF = 1,IDF = 0):
    if(numberOfSequencesToSearch == 0):
        numberOfSequencesToSearch = len(sequencesDatabase)
    if(similarityMethod == similarity.TEDSimilarity_measure ):
        similarities = {}
        sequencesDatabase = sequencesDatabase[0:numberOfSequencesToSearch]
        start = time.time()



        for i, sequence in enumerate(sequencesDatabase):
            sim = similarityMethod(inputSequence, sequence)
            similarities[sequencesDatabase[i]] = sim

        end = time.time()


    else:
        sequencesDatabase = sequencesDatabase[0:numberOfSequencesToSearch]
        start = time.time()
        if(len(processed_sequences_database) == 0):
            print("PREPROCESSING")
            processed_sequences_database = list(map(tokenizationMethod, sequencesDatabase))

            processed = []
            for elements in processed_sequences_database:
                processed.append(TFIDF.updateWeights(elements,processed_sequences_database,TF_method,IDF_method,TF = TF,IDF = IDF))
            processed_sequences_database = processed

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
        processedInputSequence = tokenizationMethod(inputSequence)
        for i,sequence in enumerate(processed_sequences_database):
            sim = similarityMethod(processedInputSequence, sequence)
            similarities[sequencesDatabase[i]] = sim
        end = time.time()

    from collections import Counter
    cnt = Counter(similarities)

    # Finding 3 highest values
    high = cnt.most_common(numberOfOutputs)
    from operator import itemgetter
    low = dict(sorted(similarities.items(), key=itemgetter(1))[:numberOfOutputs])


    highDict = {}
    for h in high:
        highDict[h[0]]=h[1]

    result.append(highDict)
    result.append(low)
    times.append(end - start)