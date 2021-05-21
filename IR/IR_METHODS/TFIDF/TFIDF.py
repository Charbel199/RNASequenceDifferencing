

import math
global IDF_array
IDF_array = []
def set_IDF(allElements):
    global IDF_array

    fullList = []
    for sequence in allElements:
        sequence = list(sequence.keys())
        for el in sequence:
            if el not in fullList:
                fullList.append(el)
    dict = {}
    for el in fullList:
        for sequence in allElements:
            if (el in sequence):
                try:
                    dict[el] += 1
                except:
                    dict[el] = 1

    IDF_array = dict
    print('DICT: ')
    print(dict)


# UPDATE DIMENSION WEIGHTS BASED ON TF AND IDF
def updateWeights(elements,allElements,TF_method,IDF_method,TF = 1,IDF = 0):
    global IDF_array
    if(len(IDF_array) == 0):
        set_IDF(allElements)


    try:
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
    except:
        set_IDF(allElements)
        if (TF and IDF):
            TF_measure = TF_method(elements)
            IDF_measure = IDF_method(elements, allElements)
            for key in elements:
                elements[key] = TF_measure[key] * IDF_measure[key]
            return elements
        elif (IDF):
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
    global  IDF_array

    N = len(allElements)
    for key in elements:
        counter = IDF_array[key]
        elements[key] = math.log(N/(counter))
    return elements


def IDF_log_plus_one(elements, allElements):
    global IDF_array
    N = len(allElements)
    for key in elements:
        counter = IDF_array[key]
        elements[key] = math.log(N / (counter))+1
    return elements

def IDF_absolute_log(elements, allElements):
    global IDF_array
    for key in elements:
        counter = IDF_array[key]
        elements[key] =abs(-math.log(counter))
    return elements