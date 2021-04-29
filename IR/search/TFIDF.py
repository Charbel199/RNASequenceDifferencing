

import math

def updateWeights(elements,allElements,TF_method,IDF_method,TF = 1,IDF = 0):
    if(TF and IDF):
        TF_measure = TF_method(elements)
        IDF_measure = IDF_method(elements,allElements)
        for key in elements:
            elements[key] = TF_measure[key]*IDF_measure[key]
        return elements
    elif(IDF):
        IDF_measure = IDF_method(elements, allElements)
        for key in elements:
            elements[key] = IDF_measure[key]
        return elements
    else:
        TF_measure = TF_method(elements)
        for key in elements:
            elements[key] = TF_measure[key]
        return elements





def TF_normal(elements):
    return elements

def TF_over_max(elements):
    maximum = max(elements.values())
    for key in elements:
        elements[key]=elements[key]/maximum
    return elements
def TF_log(elements):
    for key in elements:
        elements[key]=math.log(elements[key]+1)
    return elements



def IDF_log(elements, allElements):

    N = len(allElements)
    for key in elements:
        counter = 0
        for element in allElements:
            try:
                _ = element[key]
                counter+=1
            except:
                continue
        elements[key] = math.log(N/(counter))
    return elements


def IDF_log_plus_one(elements, allElements):
    N = len(allElements)
    for key in elements:
        counter = 0
        for element in allElements:
            try:
                _ = element[key]
                counter += 1
            except:
                continue
        elements[key] = math.log(N / (counter))+1
    return elements

def IDF_absolute_log(elements, allElements):

    for key in elements:
        counter = 0
        for element in allElements:
            try:
                _ = element[key]
                counter += 1
            except:
                continue
        elements[key] =abs(-math.log(counter))
    return elements