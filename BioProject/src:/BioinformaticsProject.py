from sys import argv
def read_codon_chart(codon_file):
    codon_dict = {}
    with open(codon_file, 'r') as chart:
        chart_lines = chart.readlines()
        for chart_line in chart_lines:
            values = chart_line.strip().split()
            if len(values) >= 2:
                codon = values[0]
                amino_acid = values[1]
                codon_dict[codon] = amino_acid
    return codon_dict

def read_seq_file(seq_file):
    sequence = ""
    with open(seq_file, 'r') as seq_input:
        nuc_seq = seq_input.read()
        for line in nuc_seq.splitlines():
            if not line.startswith('>'):
                sequence += line.strip().upper()
    return sequence

def translate_sequence(nucleotide_sequence, codon_table):
    amino_acid_sequence = ""
    for nuc in range(0, len(nucleotide_sequence), 3):
        codon = nucleotide_sequence[nuc:nuc+3]
        if len(codon) == 3:
            amino_acid_sequence += codon_table.get(codon)  # Adding default value to avoid None
    return amino_acid_sequence

def get_reading_frames(sequence):
    frames = []
    # Forward strand frames
    frames.append(sequence)          # Frame 1: Start from the first nucleotide
    frames.append(sequence[1:])      # Frame 2: Start from the second nucleotide
    frames.append(sequence[2:])      # Frame 3: Start from the third nucleotide

    # Reverse strand frames using reverse_complement
    rev_seq = reverse_complement(sequence)
    frames.append(rev_seq)           # Reverse Frame 1
    frames.append(rev_seq[1:])       # Reverse Frame 2
    frames.append(rev_seq[2:])       # Reverse Frame 3

    return frames

def reverse_complement(seq):
    # Dictionary mapping each nucleotide to its complement
    complement ={
        'A': 'T',
        'T': 'A',
        'G': 'C',
        'C': 'G'
    }

    # Reverse the sequence using slicing
    reversed_seq = seq[::-1]

    # Generate the complement for the reversed sequence
    reversed_complement_sequence = ''
    for nucleotide in reversed_seq:
        reversed_complement_sequence += complement[nucleotide]
    return reversed_complement_sequence
def find_proteins_with_overlaps(frame, codon_table):
    proteins = []
    start_pos = 0

    while start_pos <= len(frame) - 3:
        if frame[start_pos:start_pos + 3] == 'ATG':
            # Initialize list to keep track of all current protein starts
            current_proteins = []
            # Start a new protein sequence at the current position
            current_proteins.append("")

            for i in range(start_pos, len(frame) - 2, 3):
                codon = frame[i:i + 3]
                if codon_table.get(codon) == '-':  # Stop codon found
                    # Translate all current proteins and append them to the main list
                    for protein in current_proteins:
                        if protein:
                            proteins.append(translate_sequence(protein, codon_table) + '-')
                    start_pos = i + 3  # Move start position after the stop codon
                    break
                elif codon == 'ATG':  # Another start codon found within the current search
                    # Start a new protein sequence from this 'ATG'
                    current_proteins.append("")
                elif codon in codon_table:  # Valid codon, add to all current protein sequences
                    for j in range(len(current_proteins)):
                        current_proteins[j] += codon
                else:
                    continue  # Skip invalid codons

                if i >= len(frame) - 3:
                    # No stop codon found, and end of frame reached
                    start_pos = len(frame)  # Move start position to end to break the loop
                    break
            else:
                # Increment start_pos if no stop codon is found
                start_pos += 3
        else:
            # Not 'ATG', move to the next position
            start_pos += 3

    return proteins

def main():
    codon_file = argv[1]
    seq_file = argv[2]

    codon_table = read_codon_chart(codon_file)
    nucleotide_sequence = read_seq_file(seq_file)
    frames = get_reading_frames(nucleotide_sequence)
    all_proteins = []
    for frame in frames:
        proteins = find_proteins_with_overlaps(frame, codon_table)
        all_proteins.extend(proteins)
    for protein in all_proteins:
        print(protein)
main ()

