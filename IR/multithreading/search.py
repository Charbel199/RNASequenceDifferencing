from search import searchSimilarSequences, TFIDF
import threading
def multithread_search(sequence, sequences, methodsArray,numberOfSequencesToSearch=100,numberOfOutputs=3):
    results = []
    times = []
    threads = []
    for method in methodsArray:
        thread = threading.Thread(target=searchSimilarSequences.IR_Method, args=(sequences, sequence,results,times,method[0],method[1],method[2],method[3],0, [],numberOfOutputs,numberOfSequencesToSearch,method[4],method[5]))
        thread.start()
        threads.append(thread)


    for thread in threads:
        thread.join()


    print(results)
    print(times)
