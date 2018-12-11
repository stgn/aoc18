import sys
import numpy as np
from itertools import product

GRID_SIZE = 300, 300


def part_one(size_bests):
    x, y = size_bests[0][1:3]
    return f'{x},{y}'


def part_two(size_bests):
    x, y, size = max(size_bests)[1:]
    return f'{x},{y},{size}'


def sat_sum(sat, x, y, size):
    x = x - 1
    y = y - 1
    area = sat[x + size, y + size]
    if x >= 0:
        area -= sat[x, y + size]
    if y >= 0:
        area -= sat[x + size, y]
    if x >= 0 and y >= 0:
        area += sat[x, y]
    return area


if __name__ == '__main__':
    serial = int(sys.argv[1])

    grid = np.empty(GRID_SIZE, dtype=np.int32)

    for x, y in np.ndindex(GRID_SIZE):
        rack_id = x + 11
        power = ((y + 1) * rack_id + serial) * rack_id
        power = (power // 100) % 10 - 5
        grid[x, y] = power

    sat = grid.cumsum(axis=0).cumsum(axis=1)
    size_bests = []
    for size in range(3, 301):
        it = np.ndindex((301 - size,) * 2)
        power, x, y = max((sat_sum(sat, x, y, size), x, y) for x, y in it)
        if power < 0:
            break
        size_bests.append((power, x + 1, y + 1, size))

    print(part_one(size_bests))
    print(part_two(size_bests))
