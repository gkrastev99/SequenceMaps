from sequence import *
from scaling import *

# Minimum sequence width
min_width = 1

# Maximum sequence width
max_width = 10

# Maximum difference between scaled weight and width of a sequence
max_width_diff = 1


def main():
    sequences = []
    for i in range(10):
        sequences.append(Sequence(1, i + 1))

    compute_widths(sequences, min_width, max_width, max_width_diff)


if __name__ == "__main__":
    main()
