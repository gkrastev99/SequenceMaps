from sequence import *

max_width = 50


def compute_widths(sequences):
    scaling = {}
    for i in range(1, max_width):
        scaling[i] = []

    for sequence in sequences:
        sequence.scale(max_width)

        for s in scaling[sequence.width]:
            conflicts = []
            if sequence.overlaps(s):
                conflicts.append(s)

        closest = sequence
        dist = abs(sequence.scaled_weight - sequence.width)
        for s in conflicts:
            if abs(s.scaled_weight - s.width) < dist:
                closest = s
                dist = abs(s.scaled_weight - s.width)

        # TODO
        # Rearrange some sequences

        scaling[sequence.width].append(sequence)


def main():
    sequences = []

    compute_widths(sequences)

    print("Hello")


if __name__ == "__main__":
    main()
