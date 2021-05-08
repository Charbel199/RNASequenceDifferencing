from search import searchSimilarSequences, TFIDF
import threading
def multithread_search(sequence, sequences, methodsArray,numberOfSequencesToSearch=100,numberOfOutputs=3):
    results = []
    times = []
    threads = []
    for method in methodsArray:
        thread = threading.Thread(target=searchSimilarSequences.IR_Method, args=(sequences, sequence,results,times,method[0],method[1],method[2],method[3],0, [],80,numberOfSequencesToSearch,method[4],method[5]))
        thread.start()
        threads.append(thread)


    for thread in threads:
        thread.join()

    joinedResults = {}
    keys = set(results[0].keys())
    for result in results[1:]:
        keys.intersection_update(set(result.keys()))

    for key in list(keys):
        sum = 0
        for result in results:
            sum += result[key]
        weigth = sum/len(results)
        joinedResults[key] = weigth

    joinedResults = dict(sorted(joinedResults.items(), key=lambda item: item[1]))
    print(joinedResults)
    keys = list(joinedResults.keys())
    print(keys[:numberOfOutputs])
    print(keys[-numberOfOutputs:])
    top3 = {}
    low3 = {}
    for k in keys[:numberOfOutputs]:
        low3[k] = joinedResults[k]
    for k in keys[-numberOfOutputs:]:
        top3[k] = joinedResults[k]
    returnResults = []
    returnResults.append(top3)
    returnResults.append(low3)


    print(returnResults)
    print(times)
    return  returnResults,times

