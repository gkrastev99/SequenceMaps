import numpy as np

class Sequence:
    def __init__(self, locations, weight, color="black"):
        self.locations = locations  # List of location objects
        self.weight = weight
        self.color = color

        self.edges = [[locations[i], locations[i + 1]] for i in range(len(locations) - 1)]  # List of edges
        set_of_edges = set(tuple(e) for e in self.edges)
        set_of_reverse_edges = set(tuple(reversed(e)) for e in self.edges)
        self.edge_tuples = set_of_edges.union(set_of_reverse_edges)  # Set of all edges (i, j) and their reverse (j, i)

        self.scaled_weight = None  # Weight after min-max normalization
        self.width = None

    # Draw the sequence in the given plot.
    def draw(self, plot, bendmatrix, name2idx):
        for location in self.locations:
            plot.circle(location.x, location.y, size=self.width, color=self.color)

        for edge in self.edges:
            bends = np.array(bendmatrix[name2idx[edge[0].name]][name2idx[edge[1].name]])

            plot.line([edge[0].x, *(bends.T[0]), edge[1].x], [edge[0].y, *(bends.T[1]), edge[1].y], line_width=self.width, color=self.color)

    # Returns whether sequences s1 and s2 share an edge, also checking reverse order.
    @staticmethod
    def share_edge(s1, s2):
        return not s1.edge_tuples.isdisjoint(s2.edge_tuples)

