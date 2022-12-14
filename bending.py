import numpy as np  # lots of usefull linear algebra stuff
from location import *
from scaling import *


class Bending:
    loc_radius = 0

    def __init__(self, obs_buffer_dist, bend_smoothness):
        self.obs_buffer_dist = obs_buffer_dist
        self.bend_smoothness = bend_smoothness

    """--------------------------------------------------------------------"""
    """------------------------- HELPER FUNCTIONS -------------------------"""
    """--------------------------------------------------------------------"""

    # Standard formula for the angle between two vectors
    def vecAngle(self, v1, v2):
        angle = np.arccos(np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2)))
        if v2[1] > 0:
            angle = -angle
        return angle

    # Standard way to create rotation matrices
    def rMatrix(self, angle):
        return np.array(
            [[np.cos(angle), -np.sin(angle)], [np.sin(angle), np.cos(angle)]]
        )

    # tr
    def trans_rot(self, edge):
        p1, p2 = np.array(edge)
        # Transform such that p1 becomes origin
        T = p1
        # Find the angle that p2 makes with the positive x-axis
        angle = self.vecAngle([1, 0], p2 - T)
        # Get rotation matrix to make p2 land on the positive x-axis
        R = self.rMatrix(angle)

        return T, R

    # The distance between an edge and an obstacle
    def dist(self, edge, obs, line_width):
        p1, p2 = np.array(edge)

        # Distance from line (edge) to point (location)
        if len(obs) == 1:
            loc = obs[0]
            # Distance from location to endpoints of edge
            # dp1 = np.linalg.norm(p1 - loc)
            # dp2 = np.linalg.norm(p2 - loc)

            T, R = self.trans_rot(edge)

            # p2 and loc coordinates in translated and rotated scenario
            p2_tr = np.matmul(R, p2 - T)
            loc_tr = np.matmul(R, loc - T)

            # The distance from the point to the line is the
            # absolute y value in the translated and rotated scenario,
            # but we only consider that when we are between the endpoints
            dline = 9 ** 99
            if loc_tr[0] > 0 and loc_tr[0] < p2_tr[0]:
                dline = np.abs(loc_tr[1])

            # The minimum of all these is the distance from the edge to the point
            return dline  # np.min([dp1, dp2, dline])

        else:  # The distance between an line and a polygon (obstacle)
            min = 9 ** 99

            # The minimum distance from the line to each point that defines the polygon
            for pt in obs:
                min = np.min([min, self.dist(edge, [pt], line_width)])

            # The minimum distance from a sufficient sample of points (SLICES)
            # on the edge to every edge that defines the polygon
            SLICES = (
                int(np.linalg.norm(p1 - p2) / (line_width + self.obs_buffer_dist)) + 1
            )
            for i in range(len(obs) - 1):
                dir = np.array(p2 - p1)
                for v in range(SLICES + 1):
                    min = np.min(
                        [
                            min,
                            self.dist(
                                [obs[i], obs[i + 1]],
                                [p1 + (dir * (v / SLICES))],
                                line_width,
                            ),
                        ]
                    )

            return min

    # The distance from a line (list of points) to an obstacle
    def linedist(self, line, obs, lw):

        min = 9 ** 99

        for i in range(len(line) - 1):
            edge = [line[i], line[i + 1]]

            min = np.min([min, self.dist(edge, obs, lw)])

        return min

    """--------------------------------------------------------------------"""
    """-------------------------- QUALITY MEASURE -------------------------"""
    """--------------------------------------------------------------------"""

    def quality(self, obstacles, bendmatrix, name2idx, name2coord):

        # If we want little bit more than buffer
        factor = 1.0

        # Number of obstacles crossed by the graph
        Q_count = 0
        # Sum of distance needed to be outside of the buffer zone of the object
        # "How far away we are from a perfect solution"
        Q_sum = 0

        # List of locations (want to avoid other locations too)
        locs = [[loc] for loc in name2coord.values()]

        avoid = [*obstacles, *locs]

        for obs in avoid:
            for src in name2idx.keys():
                for trg in name2idx.keys():
                    if (
                        type(bendmatrix[name2idx[src]][name2idx[trg]]) == int
                    ):  # no bend. not in graph.
                        continue
                    elif bendmatrix[name2idx[src]][name2idx[trg]] == []:  # no bend.
                        line = [name2coord[src], name2coord[trg]]
                    else:  # bends
                        bends = bendmatrix[name2idx[src]][name2idx[trg]]
                        line = [name2coord[src], *bends, name2coord[trg]]

                    # If the line is close to the obstacle
                    if self.linedist(line, obs, 0) < self.obs_buffer_dist * factor:
                        # increment
                        Q_count = Q_count + 1
                        # add the distance to the edge of the buffer zone to the sum
                        Q_sum = Q_sum + (
                            self.obs_buffer_dist * factor - self.linedist(line, obs, 0)
                        )

        return Q_count, Q_sum

    """--------------------------------------------------------------------"""
    """---------------------------- BENDPOINTS ----------------------------"""
    """--------------------------------------------------------------------"""

    def bendpoints_tr(self, edge, obs, lw):
        edge = np.array(edge)
        obs = np.array(obs)

        # The [translation] and [rotation matrix] for this edge:
        # For p1, p2 = edge,
        # - p1 will become the origin
        # - p2 will be rotated onto the positive x-axis
        T, R = self.trans_rot(edge)

        # The translated and rotated object
        obs_tr = np.matmul(R, (obs - T).T).T

        if len(obs_tr) == 1:  # location, also use radius
            # intuition: circle with center [loc]
            loc = obs_tr[0]
            min_x = loc[0] - self.loc_radius - self.obs_buffer_dist
            max_x = loc[0] + self.loc_radius + self.obs_buffer_dist
            min_y = loc[1] - lw - self.loc_radius - self.obs_buffer_dist
            max_y = loc[1] + lw + self.loc_radius + self.obs_buffer_dist
        else:  # obs.T[0] gets all x values, obs.T[1] the y values
            # intuition: AABB is minimum x of all points, maximum x, ... y
            min_x = np.min(obs_tr.T[0]) - self.obs_buffer_dist
            max_x = np.max(obs_tr.T[0]) + self.obs_buffer_dist
            min_y = np.min(obs_tr.T[1]) - lw - self.obs_buffer_dist
            max_y = np.max(obs_tr.T[1]) + lw + self.obs_buffer_dist

        if min_y > 0 or max_y < 0:
            return 4 * [[0, 0]]

        # The midpoints of the bend will be:
        # consecutive in x value, and the smallest absolute y
        midpoints = []
        for x in [min_x, max_x]:
            y = min_y if np.abs(min_y) <= np.abs(max_y) else max_y
            midpoints.append([x, y])

        # TODO: lock to edge start and end if they are 'too close'
        # Want to find the x value of translated and rotated p2,
        # to be used as a clamp on the x value of the end of the bend
        p2 = edge[1]
        p2_tr = np.matmul(R, p2 - T)

        # The start and end of the bend
        start = [np.max([min_x - self.bend_smoothness, 0]), 0]
        end = [np.min([max_x + self.bend_smoothness, p2_tr[0]]), 0]

        # Combine start, midpoints and end
        bendpoints_tr = np.array([start, *midpoints, end])

        return bendpoints_tr

    """--------------------------------------------------------------------"""
    """---------------------------- BENDMATRIX ----------------------------"""
    """--------------------------------------------------------------------"""

    # Returns a |locations|??|locations| matrix describing the points that an
    # edge between two locations goes through. Only computed for existing edges
    # in the given sequences, not every single possible pair.
    def bendmatrix(self, sequences, locations, obstacles):
        # The list of sequences sorted from highest weight to lowest
        # This allows us to only look at the highest weight sequences that runs
        # along the given edge, because smaller ones will not cause more bends
        sequences = sorted(sequences, reverse=True, key=lambda x: x.weight)

        # Avoid the onion around other locations
        # Simply the largest onion for now
        self.loc_radius = 0  # sequences[0].width

        # Initialising the bendmatrix with all None values
        bendmatrix = np.zeros((len(locations), len(locations)), dtype=list)

        # Dictionaries mapping location names to coordinates and indices
        name2coord = dict()
        name2idx = dict()
        for i in range(len(locations)):
            name2coord[locations[i].name] = [locations[i].x, locations[i].y]
            name2idx[locations[i].name] = i

        # Going through the sequences to make the matrix
        for sequence in sequences:
            locs = sequence.locations
            line_width = sequence.width * 0.00445

            # Every pair of locations in the sequence means an edge
            for i in range(len(locs) - 1):
                src = locs[i]
                trg = locs[i + 1]

                # If there is a list in this cell instead of None, a higher
                # weight sequence has already been considered for this edge
                if type(bendmatrix[name2idx[src.name]][name2idx[trg.name]]) != int:
                    continue

                # The edge as a pair of coordinates
                edge = [name2coord[src.name], name2coord[trg.name]]

                # The locations in the instance that are not the endpoints of the current edge
                other_loc = [
                    [name2coord[loc]]
                    for loc in list(name2coord.keys())
                    if loc != src.name and loc != trg.name
                ]
                # All the objects to avoid
                avoid = [*obstacles, *other_loc]

                # Accumulator for all the bends for this edge, in the source to target direction
                st = []

                # Check the distance from this edge to all obstacles
                # If it is within line width and buffer, add the bend to the accumulator
                # N.B. The bendpoints are still in the translated and rotated coordinate system
                for obs in avoid:
                    if (
                        self.dist(edge, obs, line_width)
                        < line_width + self.obs_buffer_dist
                    ):
                        bend = self.bendpoints_tr(edge, obs, line_width)
                        st.extend([bend])

                # Sort all the bends on the x coordinate of the first point
                st.sort(key=lambda x: x[0][0])

                # st is a list of bends, want to 'unpack' the bends so it becomes
                # a list of points that made up the bends (preserving order)
                acc = []
                for bend in st:
                    for pt in bend:
                        acc.append(pt)
                st = np.array(acc)

                # If the last point of a bend has a larger x coordinate than
                # the first point of the next bend, 'combine' the bends by
                # setting the last point of the first bend equal to the third
                # point of the first bend, and setting the first point of the
                # second bend equal to the second point of the second bend.
                for i in range(3, len(st) - 2, 4):
                    if st[i][0] > st[i + 1][0]:
                        st[i] = st[i - 1]
                        st[i + 1] = st[i + 2]

                # Translation and rotation matrix to go back to original coordinate system
                T, R = self.trans_rot(edge)

                # If there is no bend necessary, st will be an empty list.
                # Gives an error with NumPy matrix multiplication.
                if list(st):
                    line = np.matmul(R.T, st.T).T + T
                else:
                    line = st

                # Lastly, assign the list of points for this edge to the appropriate matrix cell
                bendmatrix[name2idx[src.name]][name2idx[trg.name]] = line
                # And also assign it to the reverse edge,
                # to ensure the same bends and save computation
                bendmatrix[name2idx[trg.name]][name2idx[src.name]] = line[::-1]

        print(self.quality(obstacles, bendmatrix, name2idx, name2coord))

        # The matrix, and how to read it
        return bendmatrix, name2idx
