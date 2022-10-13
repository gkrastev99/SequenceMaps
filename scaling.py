from sequence import *
from ortools.linear_solver import pywraplp


# Compute the widths of the sequences from their weights.
def compute_widths(sequences, min_width, max_width, max_width_diff):
    scale_weights(sequences, min_width, max_width)

    # Sort the sequences by ascending weight
    sorted_sequences = sorted(sequences, key=lambda x: x.scaled_weight)

    # Compute widths using linear programming
    widths = solve_lp(sorted_sequences, min_width, max_width, max_width_diff)

    # Assign computed widths to sequences
    for i in range(len(sorted_sequences)):
        sorted_sequences[i].width = widths[i]


# Use min-max normalization to scale the weight of each sequence to the range [min_width, max_width].
def scale_weights(sequences, min_width, max_width):
    min_weight = min(sequences, key=lambda x: x.weight).weight
    max_weight = max(sequences, key=lambda x: x.weight).weight

    old_range = max_weight - min_weight
    new_range = max_width - min_width

    for s in sequences:
        s.scaled_weight = min_width + new_range * (s.weight - min_weight) / old_range


# Use linear programming to find most suitable widths for the sequences.
# Constraints:
# 1. Keep widths within the range [min_width, max_width].
# 2. Change scaled weights by at most max_width_diff.
# 3. Maintain width order.
# Objective function:
# - Optimize width difference between sequences with similar scaled weight that share an edge (aim for at least 1).
# - Minimize differences between scaled weights and computed widths (to keep width distribution similar).
def solve_lp(sorted_sequences, min_width, max_width, max_width_diff):
    # Create a solver
    solver = pywraplp.Solver("Optimize sequence widths", pywraplp.Solver.GLOP_LINEAR_PROGRAMMING)

    widths = []
    width_diffs = []
    for i in range(len(sorted_sequences)):
        # Create width variable w_i for sequence i with range satisfying constraints 1 and 2
        widths.append(solver.NumVar(max(1, sorted_sequences[i].scaled_weight - max_width_diff),
                                    min(sorted_sequences[i].scaled_weight + max_width_diff, max_width),
                                    f"w_{i}"))

        # The width of a sequence must be at least the width of the previous sequence (constraint 3)
        if i != 0:
            solver.Add(widths[i] >= widths[i - 1])

        # Create width difference variable wd_i for sequence i
        # Represents the difference between the scaled weight and width of sequence i
        width_diffs.append(solver.NumVar(0, max_width_diff, f"wd_{i}"))

        # Set wd_i equal to |w_i - scaled_weight_i|
        diff = widths[i] - sorted_sequences[i].scaled_weight
        solver.Add(width_diffs[i] >= diff)
        solver.Add(width_diffs[i] >= -diff)

    # Compute list of pairs of (possibly) conflicting sequences [i, j] with j > i
    # Two sequences i and j possibly conflict if w_j - w_i could be smaller than 1
    # We only need to keep at most one conflict for each sequence because of transitivity
    conflicts = []
    for i in range(len(sorted_sequences) - 1):
        j = i + 1
        while j < len(sorted_sequences) \
                and sorted_sequences[j].scaled_weight - sorted_sequences[i].scaled_weight < 2 * max_width_diff:
            if Sequence.conflict(sorted_sequences[i], sorted_sequences[j]):
                conflicts.append([i, j])
                break
            j += 1

    # Compute x = min(1, w_j - w_i) for conflict [i, j]
    # Inspiration from: https://or.stackexchange.com/questions/1160/how-to-linearize-min-function-as-a-constraint
    X = [solver.NumVar(0, 1, f"X_{i}") for i in range(len(conflicts))]
    x1 = 1
    x2 = [widths[conflict[1]] - widths[conflict[0]] for conflict in conflicts]
    y = solver.BoolVar("y")
    M = 5
    for x in x2:
        solver.Add(x - x1 <= M * y)
        solver.Add(x1 - x <= M * (1 - y))
    for i in range(len(X)):
        solver.Add(X[i] <= 1)
        solver.Add(X[i] <= x2[i])
        solver.Add(X[i] >= x1 - M * (1 - y))
        solver.Add(X[i] >= x2[i] - M * y)

    # Set conflict penalties
    conflict_pens = [1 - x for x in X]

    # Minimize sum of width differences and conflict penalties
    solver.Minimize(sum(width_diffs) + 2 * sum(conflict_pens))

    status = solver.Solve()

    # If an optimal solution has been found, print results
    if status == pywraplp.Solver.OPTIMAL:
        print("============= Solution linear program =============")
        print(f"Optimal value = {solver.Objective().Value()}\n")
        print("Sequence widths:")
        for i in range(len(widths)):
            print(f"s_{i}: {sorted_sequences[i].scaled_weight} -> {widths[i].solution_value()}")
        print()
        print(f"Solved in {solver.wall_time():.2f} milliseconds in {solver.iterations()} iterations")
        print("===================================================")
    else:
        print("The solver could not find an optimal solution to the linear program")

    return [width.solution_value() for width in widths]