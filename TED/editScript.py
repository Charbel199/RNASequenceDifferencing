from collections import deque

import params
import updateLogic
import utils


# Getting possible previous nodes from current node
def possiblePreviousNodes(currentNode, distArr, sourceArr, destinationArr, medicalSimilarity=0):
    epsilon = 0.05  # Used since we are working with floating numbers
    previousNodes = []

    # Current distance array coordinates and value
    currX = currentNode[0]
    currY = currentNode[1]
    currValue = distArr[currX][currY]

    # If at the start of the dist array, no previous nodes
    if currX == 0 and currY == 0:
        return []

    # Left cell coordinate
    fromInsertX = currX
    fromInsertY = currY - 1
    # Left cell value
    fromInsertValue = distArr[fromInsertX, fromInsertY]

    # Top cell coordinates
    fromDeleteX = currX - 1
    fromDeleteY = currY
    # Top cell value
    fromDeleteValue = distArr[fromDeleteX, fromDeleteY]

    # Top-left diagonal cell coordinates
    fromUpdateX = currX - 1
    fromUpdateY = currY - 1
    # Top-left diagonal cell value
    fromUpdateValue = distArr[fromUpdateX, fromUpdateY]

    # If on first row
    if currX == 0:
        # Only inserts are possible
        previousNodes.append((fromInsertX, fromInsertY, 'Insert'))
    # If on first column
    elif currY == 0:
        # Only deletes are possible
        previousNodes.append((fromDeleteX, fromDeleteY, 'Delete'))
    else:
        # Check if insert possible
        if abs(fromInsertValue - (currValue - 1)) < epsilon:
            previousNodes.append((fromInsertX, fromInsertY, 'Insert'))

        # Check if delete possible
        if abs(fromDeleteValue - (currValue - 1)) < epsilon:
            previousNodes.append((fromDeleteX, fromDeleteY, 'Delete'))

        # For update
        if sourceArr[currX - 1] == destinationArr[currY - 1]:
            # If same node, then it's a free update
            if fromUpdateValue == currValue:
                previousNodes.append((fromUpdateX, fromUpdateY, 'Update Free'))
        else:
            # If different node
            # Get nucleotides
            sourceNode = str(sourceArr[currX - 1])
            destinationNode = str(destinationArr[currY - 1])
            # Get update value
            updateValue = updateLogic.updateNode(sourceNode, destinationNode, medicalSimilarity=medicalSimilarity)
            # Check if update possible
            if (abs(fromUpdateValue - (currValue - updateValue)) < epsilon):
                previousNodes.append((fromUpdateX, fromUpdateY, 'Update'))
    return previousNodes


def getEditScripts(distArr, sourceArr, destinationArr, medicalSimilarity=0, oneEditScript=0):
    # Edit scripts as empty array
    editScripts = []
    # Initialize stack
    stack = deque()
    # Specify last node
    lastNode = (distArr.shape[0] - 1, distArr.shape[1] - 1)
    # Get edit scripts
    editScripts = recursivePath(stack, lastNode, distArr, sourceArr, destinationArr, editScripts,
                                medicalSimilarity=medicalSimilarity, oneEditScript=oneEditScript)
    return editScripts


def recursivePath(stack, currentNode, distArr, sourceArr, destinationArr, editScripts, medicalSimilarity=0,
                  oneEditScript=0):
    # If we need only one edit script and we've already got it: Stop processing and return
    if (oneEditScript and len(editScripts) == 1):
        return editScripts

    # Append current node to stack
    stack.append(currentNode)
    # Get possible previous nodes
    prevNodes = possiblePreviousNodes(currentNode, distArr, sourceArr, destinationArr,
                                      medicalSimilarity=medicalSimilarity)
    # Repeat algorithm for all previous nodes
    for prevNode in prevNodes:
        recursivePath(stack, prevNode, distArr, sourceArr, destinationArr, editScripts,
                      medicalSimilarity=medicalSimilarity, oneEditScript=oneEditScript)

    # If got to this point: No more previous nodes found
    # If the last node we're at is the starting node: Edit Script Done
    if currentNode[0] == 0 and currentNode[1] == 0:
        script = formatEditSript(list(stack), destinationArr, sourceArr)
        editScripts.append(script)
        if (oneEditScript and len(editScripts) == 1):
            return editScripts

    # Pop last node and repeat process if stack is not empty
    stack.pop()

    # If stack empty: Done OR if we only want one edit script and already got it
    if not stack or (oneEditScript and len(editScripts) == 1):
        return editScripts


# Formatting script to meaningful tuples which will be stored later in XML files
def formatEditSript(script, destinationArr, sourceArr):
    for i, node in enumerate(script):
        # First element in script is usually the bottom right final cell, no specific operation in it since it's the final cell
        if i == 0:
            script[i] = ()
        else:
            # Format into tuples
            operation = script[i][2]
            if operation == 'Insert':
                script[i] = (node[0], node[1], operation, destinationArr[node[1]])
            if operation == 'Delete':
                script[i] = (node[0], node[1], operation, sourceArr[node[0]])
            if operation == 'Update':
                script[i] = (node[0], node[1], operation, sourceArr[node[0]], destinationArr[node[1]])
            if operation == 'Update Free':
                # Set empty tuple, meaning no action
                script[i] = ()
    # Reversing edit script
    script.reverse()
    # Remove empty tuples
    script = remove(script)
    return script


# Removes empty tuples
def remove(tuples):
    tuples = [t for t in tuples if t]
    return tuples
