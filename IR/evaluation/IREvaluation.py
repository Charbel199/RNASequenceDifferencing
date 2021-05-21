
# Return  precision and recall arrays, MAP, and F-Value
def evaluate(expectedResult, queryResult):
    # EXPECTED RESULTS are from ED-Based approach
    precisions, recalls = calculatePrecisionAndRecall(expectedResult,queryResult)
    MAP = computeMAP(expectedResult,queryResult)
    FValue = computeFValue(expectedResult,queryResult)
    return precisions,recalls,MAP,FValue



# Equations from graph

def calculatePrecisionAndRecall(expectedResult, queryResult):
    correctQuery = 0
    precisions = []
    recalls = []
    for i,key in enumerate(queryResult):
        try:
            _ = expectedResult[key]
            correctQuery += 1
        except:
            pass

        PR = correctQuery/(i+1) #i+1 num of hits so far
        R = correctQuery/len(expectedResult)
        precisions.append(PR)
        recalls.append(R)
    return precisions,recalls


def computeMAP(expectedResult, queryResult):
    precisions, recalls = calculatePrecisionAndRecall(expectedResult, queryResult)
    #Mean average precision
    MAP = 0
    for i,key in enumerate(queryResult):
        PR = precisions[i]
        try:
            _ = expectedResult[key]
            rel = 1
        except:
            rel = 0

        MAP += PR * rel

    MAP = MAP/len(expectedResult)
    return MAP



def computeFValue(expectedResult, queryResult):
    precisions, recalls = calculatePrecisionAndRecall(expectedResult, queryResult)
    finalPR = precisions[-1]
    finalR = recalls[-1]
    try:
        FValue = (2*finalPR*finalR) / (finalPR + finalR)
    except:
        FValue = 0
    return FValue