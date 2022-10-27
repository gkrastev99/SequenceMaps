from bending import *
from bokeh.io import show
from bokeh.plotting import figure
from bokeh.layouts import gridplot
import random
import distinctipy
import matplotlib

# Maps countries to coordinates
country_to_coordinates = {'Ukraine': [14, 8],
                          'Russia': [16, 14],
                          'Poland': [10, 9],
                          'Germany': [7, 8],
                          'Czech Republic': [9, 8],
                          'Italy': [9, 3],
                          'Turkey': [16, 3],
                          'Spain': [2, 4],
                          'United Kingdom': [5, 10],
                          'France': [5, 7],
                          'Slovakia': [10, 7],
                          'Moldova': [13, 7],
                          'Romania': [12, 6],
                          'Austria': [9, 7],
                          'Bulgaria': [13, 4],
                          'Netherlands': [6, 10],
                          'Switzerland': [7, 6],
                          'Lithuania': [12, 11],
                          'Belgium': [6, 8],
                          'Estonia': [12, 13],
                          'Portugal': [1, 4],
                          'Ireland': [2, 10],
                          'Sweden': [9, 14],
                          'Latvia': [12, 12],
                          'Finland': [11, 15],
                          'Denmark': [7, 12],
                          'Hungary': [10, 7],
                          'Georgia': [28, 6],
                          'Montenegro': [11, 4],
                          'Norway': [7, 14],
                          'Croatia': [9, 5],
                          'Greece': [12, 2],
                          'Serbia': [11, 5],
                          'Cyprus': [16, 1],
                          'Belarus': [13, 11]}

# Scaling parameters
min_width = 5  # Minimum sequence width
max_width = 30  # Maximum sequence width
max_width_diff = 1  # Maximum difference between scaled weight and width of a sequence
width_diff_scalar = 1  # Scalar for width difference penalty
conflict_scalar = 2  # Scalar for conflict penalty

# Bending parameters
obs_buffer_dist = 0.5
bend_smoothness = 0.1

# Color of the location dots
location_color = (0, 0, 0)

# Set random seed
random.seed(0)


def main():
    locations = []

    # Maps countries to location objects
    country_to_location = {}
    for country, coordinates in country_to_coordinates.items():
        country_to_location[country] = Location(country, coordinates[0], coordinates[1])
        locations.append(country_to_location[country])

    # Random sequences starting from Ukraine, still allows revisiting locations (so may give errors)
    sequences = []
    for i in range(5):
        locs = [country_to_location["Ukraine"]]
        for j in range(3):
            country, location = random.choice(list(country_to_location.items()))
            locs.append(location)
        sequences.append(Sequence(locs, i + 1))

    # Give each sequence a different color
    colors = distinctipy.get_colors(len(sequences), colorblind_type="Deuteranomaly")
    for i in range(len(sequences)):
        sequences[i].color = matplotlib.colors.to_hex(colors[i])

    scaling = Scaling(
        min_width, max_width, max_width_diff, width_diff_scalar, conflict_scalar
    )
    scaling.compute_widths(sequences, False)

    bending = Bending(obs_buffer_dist, bend_smoothness)
    obstacles = []
    bendmatrix, name2idx = bending.bendmatrix(sequences, locations, obstacles)

    # Plot sequence map
    plot = figure(plot_width=800, plot_height=500, title="Sequence map")
    plot.image_url(url=['maps/europe.png'], x=0, y=18, w=19, h=18)
    plot.axis.visible = False
    plot.grid.visible = False
    plot.x_range.range_padding = 0
    plot.y_range.range_padding = 0

    # Draw the sequences from large to small width
    for s in sorted(sequences, reverse=True, key=lambda x: x.width):
        s.draw(plot, bendmatrix, name2idx)

    # Draw a point for each location
    for loc in locations:
        plot.circle(loc.x, loc.y, size=max(min_width - 1, 1), color=location_color)

    full_screen_plot = gridplot([[plot]], sizing_mode='stretch_both')

    show(full_screen_plot)


if __name__ == "__main__":
    main()
