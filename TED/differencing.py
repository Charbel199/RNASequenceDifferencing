import numpy as np

import updateLogic


# Getting distance array
def differenceCalculation(sourceArr, destinationArr, medicalSimilarity=0):
    # Initializing empty distance array
    distArr = np.empty(shape=(len(sourceArr) + 1, len(destinationArr) + 1), dtype=np.float16)

    # Source index represent the row's index and destination index represent the column's index
    for sourceIndex in range(distArr.shape[0]):
        for destinationIndex in range(distArr.shape[1]):

            # Initialize first row
            if sourceIndex == 0:
                if destinationIndex == 0:
                    distArr[sourceIndex, destinationIndex] = 0
                else:
                    distArr[sourceIndex, destinationIndex] = distArr[sourceIndex, destinationIndex - 1] + 1
                continue
            # Initialize first column
            elif destinationIndex == 0:
                distArr[sourceIndex, destinationIndex] = distArr[sourceIndex - 1, destinationIndex] + 1
                continue

            # Value in left cell
            prevInsert = distArr[sourceIndex, destinationIndex - 1]
            # Value in top cell
            prevDelete = distArr[sourceIndex - 1, destinationIndex]
            # Value in top-left diagonal cell
            prevUpdate = distArr[sourceIndex - 1, destinationIndex - 1]

            # Insert and delete cost 1
            # Calculating the update cost:
            if sourceArr[sourceIndex - 1] != destinationArr[destinationIndex - 1]:
                # Source and destination nucleotide loaded
                sourceNode = str(sourceArr[sourceIndex - 1])
                destinationNode = str(destinationArr[destinationIndex - 1])
                # Get update value
                updateValue = updateLogic.updateNode(sourceNode, destinationNode, medicalSimilarity=medicalSimilarity)
            else:
                # If same nucleotide cost = 0
                updateValue = 0
            # Get minimum cost
            minimumCost = min([prevInsert + 1, prevDelete + 1, prevUpdate + updateValue])
            # Set minimum cost
            distArr[sourceIndex, destinationIndex] = minimumCost

    return distArr


# Only for testing
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
            prettyTable += str(sourceArr[sourceIndex - 1]) + '\t'
        for destinationIndex, val in enumerate(row):
            prettyTable += str(val) + '\t'
        prettyTable += '\n'
    prettyTable += '\n'
    return prettyTable
