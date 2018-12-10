# AoC 2018 Notes

These are notes on my Advent of Code 2018 solutions. Anything I think is worth remarking on for personal reference will be remarked on here.


## Day 6

The solution provided in `06.py` is pretty naive but straightforward, solving both parts by evaluating the distance to every coordinate at every point on the grid. There's a faster way of solving Part 1 using a [flood-fill](https://en.wikipedia.org/wiki/Flood_fill)-like approach at the cost of more memory:

- Create a 2D array for the grid, with each cell representing which territory controls it. Mark all cells as uncontrolled.
- Create a dict for outgoing claims, mapping a grid cell to a set of claimants.
- Make a claim for each territory's starting point (coordinates from input).
- While there are outgoing claims:
    - Move outgoing claims to incoming.
    - Clear all outgoing claims.
    - For each incoming claim:
        - If the cell at the coordinate is already controlled or tied, skip it.
        - Determine the winners. If there is only one claimant, they win by default. Otherwise, the claimants with the smallest Manhattan distance from the coordinate to their starting points win.
        - Mark the cell as being controlled by the winner if there is only one. Otherwise, mark it as a tie.
        - Make an outgoing claim for neighboring cells *for each winner*.
- Count the number of cells each territory controls, etc.

An implementation of this approach is provided in [`06_fast.py`](06_fast.py), but the code is a bit unorganized and difficult to follow. I'm not completely certain it works on all inputs, but it seems to work on my own.

By moving Part 2 related code out of the loop in the original solution, it can be optimized by simply breaking to the next point on the grid when the accumulated distance exceeds the threshold.


## Day 7

The `Scheduler` class is basically an "interactive" topological sorter based on [Kahn's algorithm](https://en.wikipedia.org/wiki/Topological_sorting#Kahn's_algorithm) that allows popping a node from the no-incoming-edges queue *or* removing a node along with its outgoing edges at almost any time. Since the problem requires completing available steps (i.e. those with all prerequisites completed) in alphabetical order, a min heap is used for the queue since it allows us to find the next step in constant time.

For Part 2, I added a simple trick to reduce the number of loop iterations by essentially performing "time travel". Instead of incrementing the current time by one, set the time to the most immediate ETA of the steps currently in progress. For my input, it determines it will take 755 seconds to complete all steps but evaluates the loop only 27 times. However, it's pretty fast regardless, so the speed gain is unnoticable.


## Day 10

I originally solved this by calculating the bounding box at each time step and checking if the difference in area changed from decreasing to increasing. Afterwards, I made some observations:

- An image is formed when the height of the bounding box is 10 units.
- The height of the bounding box decreases at a constant rate.

Thus, you can find the time it takes an image to form without stepping through time by simply solving `m * t + h = 10` for `t`, where `m` is the rate of change for the height of the bounding box, and `h` is the initial height of the bounding box. `m` is equal to the minimum Y velocity of all points minus the maximum.

Once you have found `t`, for each point, simply add its velocity multiplied by `t` to its position to form the image.