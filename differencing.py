import numpy as np
import updateLogic


def differenceCalculation(sourceArr, destinationArr, medicalSimilarity=0):
    distArr = np.empty(shape=(len(sourceArr) + 1, len(destinationArr) + 1), dtype=np.float16)

    for sourceIndex in range(distArr.shape[0]):
        for destinationIndex in range(distArr.shape[1]):

            # Initialize first row
            if sourceIndex == 0:
                if destinationIndex == 0:
                    distArr[sourceIndex, destinationIndex] = 0
                else:
                    distArr[sourceIndex, destinationIndex] = distArr[sourceIndex, destinationIndex - 1] + 1
                continue
            elif destinationIndex == 0:
                distArr[sourceIndex, destinationIndex] = distArr[sourceIndex - 1, destinationIndex] + 1
                continue

            canInsert = distArr[sourceIndex, destinationIndex - 1]
            canDelete = distArr[sourceIndex - 1, destinationIndex]
            canUpdate = distArr[sourceIndex - 1, destinationIndex - 1]
            updateValue = 0
            if sourceArr[sourceIndex - 1] != destinationArr[destinationIndex - 1]:
                sourceNode = str(sourceArr[sourceIndex - 1])
                destinationNode = str(destinationArr[destinationIndex - 1])
                updateValue = updateLogic.updateNode(sourceNode, destinationNode, medicalSimilarity=medicalSimilarity)

            determinedValue = min([canInsert + 1, canDelete + 1, canUpdate + updateValue])
            distArr[sourceIndex, destinationIndex] = determinedValue

    return distArr


# For testing
def prettyPrint(sourceArr, destinationArr, distArr):
    # Printing table
    prettyTable = '\t\t'
    for letter in destinationArr:
        prettyTable += str(letter) + '\t'
    prettyTable += '\n'
    for sourceIndex, row in enumerate(distArr):
        if sourceIndex == 0:
            prettyTable += '\t'
        else:
            prettyTable += str(sourceArr[sourceIndex -1]) + '\t'
        for destinationIndex, val in enumerate(row):
            prettyTable += str(val) + '\t'
        prettyTable += '\n'
    prettyTable += '\n'
    return prettyTable
