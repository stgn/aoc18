import sys
import numpy as np

GRID_SIZE = 300, 300


def sliding_sum(arr, wlen):
    wlen = wlen - 1
    height, width = arr.shape
    verts = np.zeros(width, np.int32)

    for i in range(wlen):
        verts += arr[i]

    for y in range(height - wlen):
        verts += arr[y + wlen]
        horiz = verts[:wlen].sum()
        for x in range(width - wlen):
            horiz += verts[x + wlen]
            yield horiz, x, y
            horiz -= verts[x]
        verts -= arr[y]


def part_one(size_bests):
    x, y = size_bests[0][1:3]
    return f'{x},{y}'


def part_two(size_bests):
    x, y, size = max(size_bests)[1:]
    return f'{x},{y},{size}'


if __name__ == '__main__':
    serial = int(sys.argv[1])

    grid = np.empty(GRID_SIZE, np.int32)

    for y, x in np.ndindex(GRID_SIZE):
        rack_id = x + 11
        power = ((y + 1) * rack_id + serial) * rack_id
        power = (power // 100) % 10 - 5
        grid[y, x] = power

    size_bests = []

    for size in range(3, 301):
        windows = sliding_sum(grid, size)
        power, x, y = max(windows)
        if power < 0:
            break
        size_bests.append((power, x + 1, y + 1, size))

    print(part_one(size_bests))
    print(part_two(size_bests))
