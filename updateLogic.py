# Update logic code
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


def updateNode(sourceNode, destinationNode, medicalSimilarity=0):
    # If medical similarity, invoke medical similarity method
    if medicalSimilarity:
        return updateNodeMedicalSimilarity(sourceNode, destinationNode)
    # Arrays containing possible values of nodes
    sourceNodeValues = []
    destinationNodeValues = []
    if sourceNode in params.specialNucleotides:
        sourceNodeValues = params.specialNucleotidesRepresentations[sourceNode]
    else:
        sourceNodeValues = [sourceNode]
    if destinationNode in params.specialNucleotides:
        destinationNodeValues = params.specialNucleotidesRepresentations[destinationNode]
    else:
        destinationNodeValues = [destinationNode]

    intersection_arr = utils.intersection(sourceNodeValues, destinationNodeValues)
    union_arr = utils.union(sourceNodeValues, destinationNodeValues)

    percentage = float(len(intersection_arr) / len(union_arr))

    updateValue = 1 - percentage
    return updateValue


'''
Medically, nucleotides are grouped in 3,
 therefore it costs 0 to transform a complex nucleotide to one of its nucleotide representation and vice versa.
'''


def updateNodeMedicalSimilarity(sourceNode, destinationNode):
    if sourceNode in params.specialNucleotides and destinationNode in params.specialNucleotides:
        return 1

    if sourceNode in params.specialNucleotides:
        sourceNodeValues = params.specialNucleotidesRepresentations[sourceNode]
    else:
        sourceNodeValues = [sourceNode]
    if destinationNode in params.specialNucleotides:
        destinationNodeValues = params.specialNucleotidesRepresentations[destinationNode]
    else:
        destinationNodeValues = [destinationNode]

    if sourceNode in destinationNodeValues or destinationNode in sourceNodeValues:
        return 0

    # If non of the conditions is satisfied
    return 1
