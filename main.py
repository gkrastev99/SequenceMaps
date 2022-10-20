from bending import *
from bokeh.io import show
from bokeh.plotting import figure
import random

# Maps countries to coordinates
country_to_coordinates = {'Ukraine': [17, 9],
                          'Russia': [18, 14],
                          'Poland': [12, 10],
                          'Germany': [9, 10],
                          'Czech Republic': [9, 7],
                          'Italy': [9, 5],
                          'Turkey': [18, 3],
                          'Spain': [2, 4],
                          'United Kingdom': [5, 11],
                          'France': [5, 7],
                          'Slovakia': [13, 8],
                          'Moldova': [17, 7],
                          'Romania': [15, 7],
                          'Austria': [8, 7],
                          'Bulgaria': [15, 5],
                          'Netherlands': [7, 10],
                          'Switzerland': [9, 6],
                          'Lithuania': [14, 11],
                          'Belgium': [7, 9],
                          'Estonia': [14, 13],
                          'Portugal': [2, 4],
                          'Ireland': [4, 11],
                          'Sweden': [12, 17],
                          'Latvia': [14, 12],
                          'Finland': [14, 16],
                          'Denmark': [12, 9],
                          'Hungary': [13, 6],
                          'Georgia': [20, 7],
                          'Montenegro': [13, 4],
                          'Norway': [10, 15],
                          'Croatia': [12, 5],
                          'Greece': [14, 2],
                          'Serbia': [14, 5],
                          'Cyprus': [19, 1],
                          'Belarus': [15, 11]}

# Scaling parameters
min_width = 5  # Minimum sequence width
max_width = 20  # Maximum sequence width
max_width_diff = 1  # Maximum difference between scaled weight and width of a sequence
width_diff_scalar = 1  # Scalar for width difference penalty
conflict_scalar = 2  # Scalar for conflict penalty

# Bending parameters
obs_buffer_dist = 0.5
bend_smoothness = 0.1

# Set random seed
random.seed(0)


def main():
    locations = []

    # Maps countries to location objects
    country_to_location = {}
    for country, coordinates in country_to_coordinates.items():
        country_to_location[country] = Location(country, coordinates[0], coordinates[1])
        locations.append(country_to_location[country])

    # Random sequences starting from Ukraine with random color, still allows revisiting locations (so may give errors)
    sequences = []
    for i in range(4):
        locs = [country_to_location["Ukraine"]]
        for j in range(3):
            country, location = random.choice(list(country_to_location.items()))
            locs.append(location)
        sequences.append(Sequence(locs, i + 1, f"#{random.randint(1,9)}{random.randint(1,9)}{random.randint(1,9)}{random.randint(1,9)}{random.randint(1,9)}{random.randint(1,9)}"))

    scaling = Scaling(
        min_width, max_width, max_width_diff, width_diff_scalar, conflict_scalar
    )
    scaling.compute_widths(sequences, False)

    bending = Bending(obs_buffer_dist, bend_smoothness)
    obstacles = []
    bendmatrix, name2idx = bending.bendmatrix(sequences, locations, obstacles)

    # Plot sequence map
    plot = figure(plot_width=800, plot_height=500, title="Sequence map")
    plot.image_url(url=['maps/europe.jpeg'], x=0, y=20, w=24, h=20)

    # Draw the sequences from large to small width
    for s in sorted(sequences, reverse=True, key=lambda x: x.width):
        s.draw(plot, bendmatrix, name2idx)

    # Draw a point for each location
    for loc in locations:
        plot.circle(loc.x, loc.y, size=5, color="pink")

    show(plot)


if __name__ == "__main__":
    main()
