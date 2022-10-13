class Sequence:
    def __init__(self, points, weight, color="black"):
        self.points = points
        self.weight = weight
        self.color = color

        self.scaled_weight = None
        self.width = None

    # Returns whether sequences s1 and s2 conflict, i.e., they share an edge.
    @staticmethod
    def conflict(s1, s2):
        # TODO
        return True
