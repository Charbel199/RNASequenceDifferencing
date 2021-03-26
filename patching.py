import xml.etree.cElementTree as ET

global insertIndices
global MAX_SIZE
MAX_SIZE = 500


# GAUCUUCC  SFAFD

def insertcounter(index):
    insertCounter = 0
    for i in insertIndices:
        if i <= index:
            insertCounter += 1
    return insertCounter


def Insert(operation, source, reverse=0):
    op = operation
    if reverse == 0:
        indices = op.findall('Index')
        for i in indices:
            if i.attrib['sourceOrDestination'] == 'Source':
                index = int(i.text)
        Nucleotide = op.find('Nucleotide').text
        insertCounter = insertcounter(index)
        print(source)
        if source[index + insertCounter] == '':
            source[index + insertCounter] = Nucleotide
        else:
            source.insert(index + insertCounter, Nucleotide)
        print(source)
        insertIndices.append(index)
    else:
        DeleteReverse(op, source)


def InsertReverse(operation, source):
    op = operation
    indices = op.findall('Index')
    for i in indices:
        if i.attrib['sourceOrDestination'] == 'Destination':
            index = int(i.text)
    Nucleotide = op.find('Nucleotide').text
    insertCounter = insertcounter(index)
    print(source)
    if source[index + insertCounter] == '':
        source[index + insertCounter] = Nucleotide
    else:
        source.insert(index + insertCounter, Nucleotide)
    print(source)
    insertIndices.append(index)


def Delete(operation, source, reverse=0):
    op = operation
    if reverse == 0:
        indices = op.findall('Index')
        for i in indices:
            if i.attrib['sourceOrDestination'] == 'Source':
                index = int(i.text)
        insertCounter = insertcounter(index)
        print(source)
        source[index + insertCounter] = ";"
        print(source)
    else:
        InsertReverse(op, source)


def DeleteReverse(operation, source):
    op = operation
    indices = op.findall('Index')
    for i in indices:
        if i.attrib['sourceOrDestination'] == 'Destination':
            index = int(i.text)
    insertCounter = insertcounter(index)
    print(source)
    source[index + insertCounter] = ";"
    print(source)


def Update(operation, source, reverse=0):
    op = operation
    indices = op.findall('Index')
    for ind in indices:
        if ind.attrib['sourceOrDestination'] == ('Source' if reverse == 0 else 'Destination'):
            index = int(ind.text)
    Nucleotides = op.findall('Nucleotide')
    for n in Nucleotides:
        if n.attrib['sourceOrDestination'] == ('Destination' if reverse == 0 else 'Source'):
            Nucleotide = n.text
    insertCounter = insertcounter(index)
    print(source)
    source[index + insertCounter] = Nucleotide
    print(source)


def patch(file, sequence, reverse=0):
    global insertIndices
    insertIndices = []
    source = sequence
    source = [char for char in source]
    source = source + [''] * MAX_SIZE
    differenceFile = file
    tree = ET.parse(differenceFile)
    root_xml = tree.getroot()
    editScript = root_xml.find('EditScript')
    operations = editScript.findall('Operation')
    for op in operations:
        operationType = op.find('OperationType').text
        if operationType == 'Insert':
            Insert(op, source, reverse)
        if operationType == 'Delete':
            Delete(op, source, reverse)
        if operationType == 'Update':
            Update(op, source, reverse)
    source = "".join(source)
    destination = source.replace(';', '')
    return destination
