class Sequence:
    scaled_weight = None
    width = None

    def __init__(self, points, weight, color):
        self.points = points
        self.weight = weight
        self.color = color

    def scale(self, n):
        self.scaled_weight = 1  # TODO
        self.width = round(self.scaled_weight)

    def overlaps(self, sequence):
        # TODO
        return False
