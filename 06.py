import fileinput
from collections import defaultdict
from itertools import starmap, product

SAFE_THRESHOLD = 10000


def _inclusify(r):
    if len(r) == 1:
        stop, = r
        return (stop + 1,)
    start, stop, *step = r
    return (start, stop + 1, *step)


def ndrange(*ranges, inclusive=False):
    ranges = ((r,) if isinstance(r, int) else r 
              for r in ranges)
    if inclusive:
        ranges = map(_inclusify, ranges)
    yield from product(*starmap(range, ranges))


def part_one(coord_areas):
    return max(coord_areas.values())


if __name__ == '__main__':
    coords = []
    with fileinput.input() as f:
        for line in f:
            x, y = map(int, line.strip().split(', '))
            coords.append((x, y))

    xs, ys = zip(*coords)
    x_range = min(xs), max(xs)
    y_range = min(ys), max(ys)

    coord_areas = defaultdict(int)
    safe_region_area = 0
    infinites = {None}

    for x, y in ndrange(x_range, y_range, inclusive=True):
        min_dist = min_coord = None
        sum_dist = 0

        for i, (a, b) in enumerate(coords):
            dist = abs(a - x) + abs(b - y)
            sum_dist += dist

            if not min_dist or dist < min_dist:
                min_coord = a, b
                min_dist = dist
            elif dist == min_dist:
                min_coord = None
                
        if x in x_range or y in y_range:
            infinites.add(min_coord)
        elif min_coord not in infinites:
            coord_areas[min_coord] += 1

        if sum_dist < SAFE_THRESHOLD:
            safe_region_area += 1

    print(part_one(coord_areas))
    print(safe_region_area)
