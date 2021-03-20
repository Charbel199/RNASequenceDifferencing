from collections import deque
import params
import utils
import updateLogic
#TODO: Work on editscript convention here
def possiblePreviousNodes(currentNode, distArr, sourceArr, destinationArr):
    previousNodes = []

    currX = currentNode[0]
    currY = currentNode[1]
    currValue = distArr[currX][currY]

    ##If at the start of the dist array
    if(currX == 0 and currY==0):
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

    ##If on first row
    if (currX == 0):
        previousNodes.append((fromInsertX, fromInsertY))
    ##If on first column
    elif (currY == 0):
        previousNodes.append((fromDeleteX, fromDeleteY))
    else:
        ##Check Insert
        if (fromInsertValue == (currValue - 1)):
            previousNodes.append((fromInsertX, fromInsertY))

        ##Check Delete
        if (fromDeleteValue == (currValue - 1)):
            previousNodes.append((fromDeleteX, fromDeleteY))

        ##Check update
        if (sourceArr[currX - 1] == destinationArr[currY - 1]):
            ##If same node
            if (fromUpdateValue == (currValue)):
                previousNodes.append((fromUpdateX, fromUpdateY))
        else:
            ##If different node


            sourceNode = str(sourceArr[currX - 1])
            destinationNode = str(destinationArr[currY - 1])
            updateValue = updateLogic.updateNode(sourceNode,destinationNode)

            if (fromUpdateValue == (currValue - updateValue)):
                previousNodes.append((fromUpdateX, fromUpdateY))

    return previousNodes



def getEditScripts(distArr, sourceArr, destinationArr):
    editScripts = []
    stack = deque()
    lastNode = (distArr.shape[0]-1, distArr.shape[1]-1)
    editScripts = recursivePath(stack,lastNode,distArr,sourceArr,destinationArr,editScripts)
    return editScripts

def recursivePath(stack,currentNode,distArr,sourceArr,destinationArr,editScripts):
    ##Append current node to stack
    stack.append(currentNode)
    ##Get possible previous nodes
    prevNodes = possiblePreviousNodes(currentNode,distArr,sourceArr,destinationArr)

    ##Repeat algorithm for all previous nodes
    for prevNode in prevNodes:
        recursivePath(stack,prevNode,distArr,sourceArr,destinationArr,editScripts)


    ##If got to this point: No more previous nodes found

    ##If the last node we're at is the starting node: Edit Script Done
    if(currentNode[0] == 0 and currentNode[1]==0):
        editScripts.append(list(stack))

    ##Pop last node
    stack.pop()

    ##If stack empty: Done
    if(not stack):
        return editScripts