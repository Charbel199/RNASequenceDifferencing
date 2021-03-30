import xml.etree.cElementTree as ET


# String manipulation methods
# Insert in string
def insert_in_sequence(sequence, index, nucleotide):
    sequence = sequence[0:index] + nucleotide + sequence[index:]
    return sequence


# Delete in string
def delete_from_sequence(sequence, index):
    sequence = sequence[0:index] + sequence[index + 1:]
    return sequence


# Update in string
def update_in_sequence(sequence, index, nucleotide):
    sequence = sequence[0:index] + nucleotide + sequence[index + 1:]
    return sequence


def Insert(sequence, sourceIndex, destinationIndex, nucleotide, reverse=0):
    # INSERT using destination index (Going from source to destination)
    if not reverse:
        sequence = insert_in_sequence(sequence, destinationIndex, nucleotide)
        return sequence
    else:
        # If we are reverse patching: then we DELETE using the source index (Going from destination to source)
        sequence = delete_from_sequence(sequence, sourceIndex)
        return sequence


def Delete(sequence, sourceIndex, destinationIndex, nucleotide, reverse=0):
    # DELETE using destination index (Going from source to destination)
    if not reverse:
        sequence = delete_from_sequence(sequence, destinationIndex)
        return sequence
    else:
        # If we are reverse patching: then we INSERT using the source index (Going from destination to source)
        sequence = insert_in_sequence(sequence, sourceIndex, nucleotide)
        return sequence


def Update(sequence, sourceIndex, destinationIndex, sourceNucleotide, destinationNucleotide, reverse=0):
    # UPDATE using destination index (Going from source to destination)
    if not reverse:
        sequence = update_in_sequence(sequence, destinationIndex, destinationNucleotide)
        return sequence
    else:
        # UPDATE using source index (Going from destination to source)
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
        # Insert operation
        if operationType == 'Insert':
            nucleotide = op.find('Nucleotide').text
            sequence = Insert(sequence, sourceIndex, destinationIndex, nucleotide, reverse)
        # Delete operation
        if operationType == 'Delete':
            nucleotide = op.find('Nucleotide').text
            sequence = Delete(sequence, sourceIndex, destinationIndex, nucleotide, reverse)
        # Update operation
        if operationType == 'Update':
            # Getting source and destination nucleotides
            nucleotides = op.findall('Nucleotide')
            for n in nucleotides:
                if n.attrib['sourceOrDestination'] == 'Source':
                    sourceNucleotide = n.text
                if n.attrib['sourceOrDestination'] == 'Destination':
                    destinationNucleotide = n.text
            sequence = Update(sequence, sourceIndex, destinationIndex, sourceNucleotide, destinationNucleotide, reverse)

    return sequence
