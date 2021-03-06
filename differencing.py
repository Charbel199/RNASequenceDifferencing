import numpy as np

def differenceCalculation(sourceArr, destinationArr):
    distArr = np.empty(shape=(len(sourceArr) + 1, len(destinationArr) + 1), dtype=np.int16)

    for sourceIndex in range(distArr.shape[0]):
        for destinationIndex in  range(distArr.shape[1]):

            ##Initialize first row
            if(sourceIndex == 0):
                if(destinationIndex == 0):
                    distArr[sourceIndex, destinationIndex] = 0
                else:
                    distArr[sourceIndex, destinationIndex] = distArr[sourceIndex, destinationIndex-1] + 1
                continue
            elif(destinationIndex == 0):
                distArr[sourceIndex, destinationIndex] = distArr[sourceIndex - 1, destinationIndex] + 1
                continue


            canInsert = distArr[sourceIndex, destinationIndex-1]
            canDelete = distArr[sourceIndex-1, destinationIndex]
            canUpdate = distArr[sourceIndex-1, destinationIndex-1]
            updateValue = 0
            if(sourceArr[sourceIndex-1] != destinationArr[destinationIndex-1]):
                updateValue = 1

            determinedValue = min([canInsert+1,canDelete+1,canUpdate+updateValue])
            distArr[sourceIndex, destinationIndex] = determinedValue

    return distArr


##For testing
def prettyPrint(sourceArr,destinationArr,distArr):
    ##Priting table
    print('\t\t', end='')
    for letter in destinationArr:
        print(letter + '\t', end='')
    print()
    for sourceIndex, row in enumerate(distArr):
        if (sourceIndex == 0):
            print('\t', end='')
        else:
            print(sourceArr[sourceIndex - 1] + '\t', end='')
        for destinationIndex, val in enumerate(row):
            print(val, end='\t')
        print()
    print()




