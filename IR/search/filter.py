from search import searchSimilarSequences
from IR_METHODS.TFIDF import TFIDF
from IR_METHODS.dimensionDefinition import tokenization
from IR_METHODS.similarityMeasures import similarity
import math


def filter(sequencesToFilter, inputSequence, sequencesAfterFilter, numberOfSequencesToSearch, operator='Range'):
    tag = tokenization.sequence_to_vector_edge
    cos = similarity.multiset_jackard_measure
    normal = TFIDF.TF_normal
    log = TFIDF.IDF_log
    times = []
    sequencesAfterFilter = searchSimilarSequences.IR_Method(sequencesToFilter, inputSequence, sequencesAfterFilter,
                                                            times,
                                                            tag, cos,
                                                            normal,
                                                            log,
                                                            numberOfOutputs=math.floor(numberOfSequencesToSearch*0.7),
                                                            numberOfSequencesToSearch=numberOfSequencesToSearch,
                                                            epsilon=1.6, operator=operator)

    sequencesAfterFilter = list(sequencesAfterFilter[0])
    return sequencesAfterFilter
