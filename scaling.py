from ortools.linear_solver import pywraplp


# Compute the widths of the sequences from their weights.
def compute_widths(sequences, min_width, max_width, max_width_diff):
    scale_weights(sequences, min_width, max_width)

    # Sort the sequences by ascending weight
    sorted_sequences = sorted(sequences, key=lambda x: x.scaled_weight)

    widths = solve_lp(sorted_sequences, min_width, max_width, max_width_diff)

    # TODO Assign computed widths to sequences
    #for i in range(len(sorted_sequences)):
     #   sorted_sequences[i].width = widths[i]


# Use min-max normalization to scale the weight of each sequence to the range [min_width, max_width].
def scale_weights(sequences, min_width, max_width):
    min_weight = min(sequences, key=lambda x: x.weight).weight
    max_weight = max(sequences, key=lambda x: x.weight).weight

    for s in sequences:
        s.scaled_weight = min_width + (max_width - min_width) * (s.weight - min_weight) / (max_weight - min_weight)


# Use linear programming to find most suitable widths for the sequences.
# Constraints:
# 1. Keep widths within the range [min_width, max_width].
# 2. Change widths by at most max_width_diff.
# 3. Maintain width order.
# Objective function: optimize width difference between overlapping sequences sharing an edge.
def solve_lp(sorted_sequences, min_width, max_width, max_width_diff):
    # Create a solver
    solver = pywraplp.Solver("Optimize sequence widths", pywraplp.Solver.GLOP_LINEAR_PROGRAMMING)

    # Create width variables w_i for the i-th sequence with range satisfying constraints 1 and 2
    widths = [solver.NumVar(max(1, sorted_sequences[i].scaled_weight - max_width_diff),
                            min(sorted_sequences[i].scaled_weight + max_width_diff, max_width),
                            f"w_{i}")
              for i in range(len(sorted_sequences))]

    # The width of a sequence must be at least the width of the previous sequence (to maintain the width order)
    for i in range(2, len(sorted_sequences)):
        solver.Add(widths[i] >= widths[i - 1])

    # TODO Minimize something
    # solver.Minimize()

    status = solver.Solve()

    # If an optimal solution has been found, print results
    if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
        print("================= Solution =================")
        print(f"Solved in {solver.wall_time():.2f} milliseconds in {solver.iterations()} iterations\n")
        print(f"Optimal value = {solver.Objective().Value()}\n")
        print("Widths:")
        for width in widths:
            print(f"{width.solution_value}")
    else:
        print('The solver could not find an optimal solution.')

    # TODO return optimized widths
