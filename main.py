from location import *
from scaling import *
from bending import *

# Scaling parameters
min_width = 1  # Minimum sequence width
max_width = 5  # Maximum sequence width
max_width_diff = 1  # Maximum difference between scaled weight and width of a sequence
width_diff_scalar = 1  # Scalar for width difference penalty
conflict_scalar = 2  # Scalar for conflict penalty

# Bending parameters
loc_radius = 0.3
obs_buffer_dist = 0.2
bend_smoothness = 0.5


def main():
    # Test input
    # source = Location("source", 0, 0)
    # l1 = Location("l1", 10, 0)
    # l2 = Location("l2", 0, 10)
    # l3 = Location("l3", 10, 10)
    # sequences = []
    # sequences.append(Sequence([source, l3, l1], 1))
    # sequences.append(Sequence([source, l1, l2], 2))
    # sequences.append(Sequence([source, l2, l1], 2))
    # sequences.append(Sequence([source, l1, l2, l3], 3))

    # Another test input
    S = Location("S", 0, 0)
    A = Location("A", 4, 4)
    B = Location("B", 4, -0.5)
    C = Location("C", 3.5, -4)
    D = Location("D", 6, 1)

    sequences = []
    sequences.append(Sequence([S, A, D], 1000))
    sequences.append(Sequence([S, B, D], 700))
    sequences.append(Sequence([S, B, C], 500))
    sequences.append(Sequence([S, A], 200))
    # sequences.append(Sequence([S, A, C], 200))

    scaling = Scaling(
        min_width, max_width, max_width_diff, width_diff_scalar, conflict_scalar
    )
    scaling.compute_widths(sequences, True)

    bending = Bending(loc_radius, obs_buffer_dist, bend_smoothness)
    locations = [S, A, B, C, D]
    # Obstacles: lists only, making a class would make things harder.
    # I'm using numpy for matrix multiplications so I can
    # translate and rotate all points of an obstacle at once.
    obstacles = [[[4, -1.5]], [[3.5, -3]], [[2, 2], [3, 1], [4, 2], [2, 2]], [[1, 1.5]]]
    bendmatrix, name2idx = bending.bendmatrix(sequences, locations, obstacles)

    # use name2idx to read the appropriate cell values of the bendmatrix

    # TODO: display the sequence map


if __name__ == "__main__":
    main()
