import fileinput
import numpy as np
from collections import defaultdict
from itertools import product

UNCLAIMED = -2
CONTESTED = -1
SAFE_THRESHOLD = 10000


def part_one(coords, w, h):
    fm = np.full((w, h), UNCLAIMED, dtype=np.int32)
    out_claims = {c: {i} for i, c in enumerate(coords)}
    infinites = {CONTESTED}

    while out_claims:
        in_claims = out_claims
        out_claims = defaultdict(set)

        for coord, claims in in_claims.items():
            if fm[coord] >= CONTESTED:
                continue

            x, y = coord

            if len(claims) == 1:
                winners = claims
            else:
                winners = min_dist = None

                for claimant in claims:
                    cx, cy = coords[claimant]
                    dist = abs(cx - x) + abs(cy - y)

                    if min_dist is None or dist < min_dist:
                        winners = [claimant]
                        min_dist = dist
                    elif dist == min_dist:
                        winners.append(claimant)

            if len(winners) > 1:
                fm[coord] = CONTESTED
            else:
                winner, = winners
                fm[coord] = winner
                if x in (0, w) or y in (0, h):
                    infinites.add(winner)

            if x > 0:
                out_claims[x - 1, y].update(winners)
            if y > 0:
                out_claims[x, y - 1].update(winners)
            if x < w - 1:
                out_claims[x + 1, y].update(winners)
            if y < h - 1:
                out_claims[x, y + 1].update(winners)

    counts = dict(zip(*np.unique(fm, return_counts=True)))
    finites = counts.keys() - infinites
    return max(counts[k] for k in finites)


def part_two(coords, w, h):
    safe_region_area = 0

    for x, y in product(range(w), range(h)):
        sum_dist = 0
        is_safe = True

        for a, b in coords:
            sum_dist += abs(a - x) + abs(b - y)
            if sum_dist >= SAFE_THRESHOLD:
                is_safe = False
                break

        safe_region_area += is_safe

    return safe_region_area


if __name__ == '__main__':
    coords = []
    with fileinput.input() as f:
        for line in f:
            x, y = map(int, line.strip().split(', '))
            coords.append((x, y))

    x_min, y_min = map(min, zip(*coords))
    x_max, y_max = map(max, zip(*coords))
    coords = [(x - x_min, y - y_min) for x, y in coords]
    w, h = x_max - x_min + 1, y_max - y_min + 1

    print(part_one(coords, w, h))
    print(part_two(coords, w, h))
