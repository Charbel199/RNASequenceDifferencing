from collections import deque
import params
import utils
import updateLogic


# TODO: Work on editscript convention here
def possiblePreviousNodes(currentNode, distArr, sourceArr, destinationArr, medicalSimilarity=0):
    previousNodes = []
    currX = currentNode[0]
    currY = currentNode[1]
    currValue = distArr[currX][currY]

    # If at the start of the dist array
    if currX == 0 and currY == 0:
        return []

    fromInsertX = currX
    fromInsertY = currY - 1
    fromInsertValue = distArr[fromInsertX, fromInsertY]

    fromDeleteX = currX - 1
    fromDeleteY = currY
    fromDeleteValue = distArr[fromDeleteX, fromDeleteY]

    fromUpdateX = currX - 1
    fromUpdateY = currY - 1
    fromUpdateValue = distArr[fromUpdateX, fromUpdateY]

    # If on first row
    if currX == 0:
        previousNodes.append((fromInsertX, fromInsertY, 'Insert'))
    # If on first column
    elif currY == 0:
        previousNodes.append((fromDeleteX, fromDeleteY, 'Delete'))
    else:
        # Check Insert
        if fromInsertValue == (currValue - 1):
            previousNodes.append((fromInsertX, fromInsertY, 'Insert'))

        # Check Delete
        if fromDeleteValue == (currValue - 1):
            previousNodes.append((fromDeleteX, fromDeleteY, 'Delete'))

        # Check update
        if sourceArr[currX - 1] == destinationArr[currY - 1]:
            # If same node
            if fromUpdateValue == currValue:
                previousNodes.append((fromUpdateX, fromUpdateY, 'Update Free'))
        else:
            # If different node

            sourceNode = str(sourceArr[currX - 1])
            destinationNode = str(destinationArr[currY - 1])
            updateValue = updateLogic.updateNode(sourceNode, destinationNode, medicalSimilarity=medicalSimilarity)

            if (fromUpdateValue - (currValue - updateValue)) < 0.05:
                previousNodes.append((fromUpdateX, fromUpdateY, 'Update'))
    return previousNodes


def getEditScripts(distArr, sourceArr, destinationArr, medicalSimilarity=0, operations=0):
    editScripts = []
    stack = deque()
    lastNode = (distArr.shape[0] - 1, distArr.shape[1] - 1)
    editScripts = recursivePath(stack, lastNode, distArr, sourceArr, destinationArr, editScripts,
                                medicalSimilarity=medicalSimilarity, operations=operations)
    return editScripts


def remove(tuples):
    tuples = [t for t in tuples if t]
    return tuples


def recursivePath(stack, currentNode, distArr, sourceArr, destinationArr, editScripts, medicalSimilarity=0,
                  operations=0):
    # Append current node to stack
    stack.append(currentNode)
    # Get possible previous nodes
    prevNodes = possiblePreviousNodes(currentNode, distArr, sourceArr, destinationArr,
                                      medicalSimilarity=medicalSimilarity)

    # Repeat algorithm for all previous nodes
    for prevNode in prevNodes:
        recursivePath(stack, prevNode, distArr, sourceArr, destinationArr, editScripts,
                      medicalSimilarity=medicalSimilarity, operations=operations)

    # If got to this point: No more previous nodes found

    # If the last node we're at is the starting node: Edit Script Done
    if currentNode[0] == 0 and currentNode[1] == 0:
        script = list(stack)
        if operations == 1:
            for i, node in enumerate(script):
                if i == 0:
                    script[i] = ()
                else:
                    operation = script[i][2]
                    if operation == 'Insert':
                        script[i] = (node[0], node[1], operation, destinationArr[node[1]])
                    if operation == 'Delete':
                        script[i] = (node[0], node[1], operation, sourceArr[node[0]])
                    if operation == 'Update':
                        script[i] = (node[0], node[1], operation, sourceArr[node[0]], destinationArr[node[1]])
                    if operation == 'Update Free':
                        script[i] = ()

        script.reverse()
        script = remove(script)
        editScripts.append(script)

    # Pop last node
    stack.pop()

    # If stack empty: Done
    if not stack:
        return editScripts
