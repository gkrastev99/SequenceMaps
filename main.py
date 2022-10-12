from sequence import *
from scaling import *

min_width = 1
max_width = 50
max_width_diff = 1


def main():
    sequences = [Sequence(1, 1), Sequence(1, 3), Sequence(1, 5)]

    compute_widths(sequences, min_width, max_width, max_width_diff)


if __name__ == "__main__":
    main()
