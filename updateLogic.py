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
    # If the source nucleotide is a special nucleotide
    if sourceNode in params.specialNucleotides:
        # Get all possible nucleotides of source
        sourceNodeValues = params.specialNucleotidesRepresentations[sourceNode]
    else:
        # If not special nucleotide then it's the only nucleotide possible for the source
        sourceNodeValues = [sourceNode]
    # If the destination nucleotide is a special nucleotide
    if destinationNode in params.specialNucleotides:
        # Get all possible nucleotides of destination
        destinationNodeValues = params.specialNucleotidesRepresentations[destinationNode]
    else:
        # If not special nucleotide then it's the only nucleotide possible for the destination
        destinationNodeValues = [destinationNode]

    #Get common possible nucleotides between source and destination (Intersection)
    intersection_arr = utils.intersection(sourceNodeValues, destinationNodeValues)
    #Get all possible nucleotides between source and destination (Union)
    union_arr = utils.union(sourceNodeValues, destinationNodeValues)

    #Common possible nucleotides divided by all possible nucleotides: Similarity percentage based on common nucleotides
    #Ex: [G,C] and V: [G,A,C] percentage = 2/3
    #Ex: [U] and V: [G,A,C]  percentage = 0
    percentage = float(len(intersection_arr) / len(union_arr))
    # When similarity percentage between two nucleotides is higher, cost is lower, and vice versa
    updateValue = 1 - percentage
    return updateValue


'''
Medically, nucleotides are grouped in 3,
 therefore it costs 0 to transform a complex nucleotide to one of its nucleotide representation and vice versa.
'''


def updateNodeMedicalSimilarity(sourceNode, destinationNode):
    # It costs 1 to update a special nucleotide to another special nucleotide
    if sourceNode in params.specialNucleotides and destinationNode in params.specialNucleotides:
        return 1
    #If the source nucleotide is a special nucleotide
    if sourceNode in params.specialNucleotides:
        #Get all possible nucleotides of source
        sourceNodeValues = params.specialNucleotidesRepresentations[sourceNode]
    else:
        #If not special nucleotide then it's the only nucleotide possible for the source
        sourceNodeValues = [sourceNode]
    # If the destination nucleotide is a special nucleotide
    if destinationNode in params.specialNucleotides:
        # Get all possible nucleotides of destination
        destinationNodeValues = params.specialNucleotidesRepresentations[destinationNode]
    else:
        # If not special nucleotide then it's the only nucleotide possible for the destination
        destinationNodeValues = [destinationNode]

    #If source nucleotide included in destination nucleotide or vice versa then cost is 0
    if sourceNode in destinationNodeValues or destinationNode in sourceNodeValues:
        return 0

    # If none of the conditions is satisfied, cost is 1
    return 1
