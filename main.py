from location import *
from scaling import *

# Scaling parameters
min_width = 1  # Minimum sequence width
max_width = 5  # Maximum sequence width
max_width_diff = 1  # Maximum difference between scaled weight and width of a sequence
width_diff_scalar = 1  # Scalar for width difference penalty
conflict_scalar = 2  # Scalar for conflict penalty


def main():
    # Test input
    source = Location("source", 0, 0)
    l1 = Location("l1", 10, 0)
    l2 = Location("l2", 0, 10)
    l3 = Location("l3", 10, 10)
    sequences = []
    sequences.append(Sequence([source, l3, l1], 1))
    sequences.append(Sequence([source, l1, l2], 2))
    sequences.append(Sequence([source, l2, l1], 2))
    sequences.append(Sequence([source, l1, l2, l3], 3))

    scaling = Scaling(min_width, max_width, max_width_diff, width_diff_scalar, conflict_scalar)
    scaling.compute_widths(sequences, True)


if __name__ == "__main__":
    main()
