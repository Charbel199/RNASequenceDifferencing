from similarityMeasures import similarity
import time
def IR_Method(sequencesDatabase,inputSequence,result,times,tokenizationMethod,similarityMethod,preprocessed = 0,processed_sequences_database = [],numberOfOutputs = 3,numberOfSequencesToSearch = 0):
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
        if(not processed_sequences_database):
            processed_sequences_database = map(tokenizationMethod, sequencesDatabase)

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


    result.append(high)
    result.append(low)
    times.append(end - start)