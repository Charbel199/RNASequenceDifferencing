import xml.etree.ElementTree as ET
import lxml.etree as et
import xml.etree.cElementTree as parser


def prettyPrint(fileName):
    myFile = fileName
    tree = et.parse(myFile)
    pretty = et.tostring(tree, encoding="unicode", pretty_print=True)
    file = open(myFile, 'w')
    file.write(pretty)
    file.close()


def differencing(editScripts):
    RNADifferencing = ET.Element('RNADifferencing')
    for es in editScripts:
        EditScript = ET.SubElement(RNADifferencing, 'EditScript')
        for op in es:
            Operation = ET.SubElement(EditScript, 'Operation')
            OperationType = ET.SubElement(Operation, 'OperationType')
            OperationType.text = op[2]
            IndexSource = ET.SubElement(Operation, 'Index')
            IndexSource.set('sourceOrDestination', 'Source')
            IndexSource.text = str(op[0])
            IndexDestination = ET.SubElement(Operation, 'Index')
            IndexDestination.set('sourceOrDestination', 'Destination')
            IndexDestination.text = str(op[1])
            Nucleotide = ET.SubElement(Operation, 'Nucleotide')
            if op[2] == 'Update':
                Nucleotide.set('sourceOrDestination', 'Source')
            Nucleotide.text = op[3]
            if len(op) == 5:
                Nucleotide = ET.SubElement(Operation, 'Nucleotide')
                Nucleotide.set('sourceOrDestination', 'Destination')
                Nucleotide.text = op[4]
    myData = ET.tostring(RNADifferencing, encoding="unicode")
    fileName = "XML.xml"
    myFile = open(fileName, "w")
    myFile.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>" + myData)
    myFile.close()
    prettyPrint(fileName)


def sequenceExtraction(fileName):
    tree = ET.parse(fileName)
    sequence = tree.getroot().find('RNA').find('sequence').text.strip()
    return sequence
