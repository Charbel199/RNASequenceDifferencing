from search import searchSimilarSequences
from IR_METHODS.TFIDF import TFIDF
from IR_METHODS.dimensionDefinition import tokenization
from IR_METHODS.similarityMeasures import similarity
import math


def filter(sequencesToFilter, inputSequence, sequencesAfterFilter, numberOfSequencesToSearch):
    tag = tokenization.sequence_to_vector_tag
    cos = similarity.vector_cosine_measure
    normal = TFIDF.TF_normal
    log = TFIDF.IDF_log
    times = []
    sequencesAfterFilter = searchSimilarSequences.IR_Method(sequencesToFilter, inputSequence, sequencesAfterFilter,
                                                            times,
                                                            tag, cos,
                                                            normal,
                                                            log,
                                                            numberOfSequencesToSearch=numberOfSequencesToSearch,
                                                            epsilon=1.05, operator='Range')
    sequencesAfterFilter = list(sequencesAfterFilter[0])
    return sequencesAfterFilter
