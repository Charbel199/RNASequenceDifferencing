from Bio import SeqIO


# .fa file to LIST of sequences
def parse_fa(input_file):
    fasta_sequences = SeqIO.parse(open(input_file),'fasta')
    RNA_sequences = []
    for fasta in fasta_sequences:
        # RNA and NOT DNA
        RNA_sequences.append(str(fasta.seq).replace("T", "U"))
    return RNA_sequences


if(__name__ == "__main__"):
    RNA_sequences = parse_fa('../humanRNA.fa')
    print(len(RNA_sequences))