#Update logic code
import params
import utils

'''
Complex logic here
- R represents G or A (purine)
- M represents A or C (amino)
- S represents G or C
- V represents G, A, or C
- N represents G, U, A, or C. In other words, N basically represents any canonical nucleotide base.
Assumption: If probability higher: Cost less
Cost = 1 - Proba
'''

def updateNode(sourceNode, destinationNode):
    # Arrays containing possible values of nodes
    sourceNodeValues = []
    destinationNodeValues = []
    if (sourceNode in params.specialNucleotides):
        sourceNodeValues = params.specialNucleotidesRepresentations[sourceNode]
    else:
        sourceNodeValues = [sourceNode]
    if (destinationNode in params.specialNucleotides):
        destinationNodeValues = params.specialNucleotidesRepresentations[destinationNode]
    else:
        destinationNodeValues = [destinationNode]

    intersection_arr = utils.intersection(sourceNodeValues, destinationNodeValues)
    union_arr = utils.union(sourceNodeValues, destinationNodeValues)

    percentage = float(len(intersection_arr) / len(union_arr))

    updateValue = 1 - percentage
    return updateValue