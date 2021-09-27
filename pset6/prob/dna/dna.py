from csv import reader, DictReader
from sys import argv, exit


def main():

    if len(argv) != 3:
        print("Usage: python dna.py data.csv sequence.txt")
        exit(1)

    # open csvfile
    with open(argv[1], "r") as csvfile:
        reader = DictReader(csvfile)
        dna_data = list(reader)

    # open sequence
    with open(argv[2], "r") as file:
        sequence = file.read()

    # find longest chain

    dna_columns = len(reader.fieldnames)
    max_counts = [0]

    # add str header
    for i in range(1, dna_columns):
        dna_str = reader.fieldnames[i]
        max_counts.append(0)

        # iterate through the sequence
        for j in range(len(sequence)):
            temp_str_count = 0

            if sequence[j:(j + len(dna_str))] == dna_str:
                k = 0

                # how many consecutive checking
                while sequence[(j + k):(j + k + len(dna_str))] == dna_str:
                    temp_str_count += 1
                    k += len(dna_str)

                if temp_str_count > max_counts[i - 1]:
                    max_counts[i - 1] = temp_str_count

    # compare with database
    for i in range(len(dna_data)):
        matches = 0

        for j in range(1, dna_columns):

            if int(max_counts[j - 1]) == int(dna_data[i][reader.fieldnames[j]]):
                matches += 1

            if matches == (dna_columns - 1):
                print(dna_data[i]['name'])
                exit(0)

    print("No Match")


main()
