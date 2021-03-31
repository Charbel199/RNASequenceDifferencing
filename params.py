'''
Complex logic here
- R represents G or A (purine)
- M represents A or C (amino)
- S represents G or C
- V represents G, A, or C
- N represents G, U, A, or C. In other words, N basically represents any canonical nucleotide base.
Assumption: If probability higher: Cost less
Cost = 1 - Proba
R/M/S update cost: 1/2
V update cost: 2/3
N update cost: 3/4
'''

specialNucleotides = ['R', 'M', 'S', 'V', 'N']
specialNucleotidesRepresentations = {
    'R': ['G', 'A'],
    'M': ['A', 'C'],
    'S': ['G', 'C'],
    'V': ['G', 'A', 'C'],
    'N': ['G', 'U', 'A', 'C']
}

allPossibleNucleotides = ['R', 'M', 'S', 'V', 'N', 'G', 'U', 'A', 'C']
