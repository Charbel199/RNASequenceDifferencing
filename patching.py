import xml.etree.cElementTree as ET


def insert_in_sequence(sequence, index, nucleotide):
    if index == len(sequence):
        sequence = sequence + nucleotide
        return sequence
    sequence = sequence[0:index] + nucleotide + sequence[index:]
    return sequence


def delete_from_sequence(sequence, index):
    sequence = sequence[0:index] + sequence[index + 1:]
    return sequence


def update_in_sequence(sequence, index, nucleotide):
    sequence = sequence[0:index] + nucleotide + sequence[index + 1:]
    return sequence


def Insert(sequence, sourceIndex, destinationIndex, nucleotide, reverse=0):
    if not reverse:
        sequence = insert_in_sequence(sequence, destinationIndex, nucleotide)
        return sequence
    else:
        sequence = delete_from_sequence(sequence, sourceIndex)
        return sequence


def Delete(sequence, sourceIndex, destinationIndex, nucleotide, reverse=0):
    if not reverse:
        sequence = delete_from_sequence(sequence, destinationIndex)
        return sequence
    else:
        sequence = insert_in_sequence(sequence, sourceIndex, nucleotide)
        return sequence


def Update(sequence, sourceIndex, destinationIndex, sourceNucleotide, destinationNucleotide, reverse=0):
    if not reverse:
        sequence = update_in_sequence(sequence, destinationIndex, destinationNucleotide)
        return sequence
    else:
        sequence = update_in_sequence(sequence, sourceIndex, sourceNucleotide)
        return sequence


def patch(file, sequence, reverse=0):
    differenceFile = file
    # Parse XML
    tree = ET.parse(differenceFile)
    root_xml = tree.getroot()
    editScript = root_xml.find('EditScript')
    # Get all operations
    operations = editScript.findall('Operation')
    for op in operations:
        # Getting operation, source index and destination index.
        operationType = op.find('OperationType').text
        indices = op.findall('Index')
        for i in indices:
            if i.attrib['sourceOrDestination'] == 'Source':
                sourceIndex = int(i.text)
            if i.attrib['sourceOrDestination'] == 'Destination':
                destinationIndex = int(i.text)

        if operationType == 'Insert':
            nucleotide = op.find('Nucleotide').text
            sequence = Insert(sequence, sourceIndex, destinationIndex, nucleotide, reverse)

        if operationType == 'Delete':
            nucleotide = op.find('Nucleotide').text
            sequence = Delete(sequence, sourceIndex, destinationIndex, nucleotide, reverse)

        if operationType == 'Update':
            nucleotides = op.findall('Nucleotide')
            for n in nucleotides:
                if n.attrib['sourceOrDestination'] == 'Source':
                    sourceNucleotide = n.text
                if n.attrib['sourceOrDestination'] == 'Destination':
                    destinationNucleotide = n.text
            sequence = Update(sequence, sourceIndex, destinationIndex, sourceNucleotide, destinationNucleotide, reverse)

    return sequence
