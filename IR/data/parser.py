from Bio import SeqIO

def parse_fa(input_file):
    fasta_sequences = SeqIO.parse(open(input_file),'fasta')
    RNA_sequences = []
    for fasta in fasta_sequences:
        RNA_sequences.append(str(fasta.seq).replace("T", "U"))
    return RNA_sequences


if(__name__ == "__main__"):
    RNA_sequences = parse_fa('../humanRNA.fa')
    print(len(RNA_sequences))