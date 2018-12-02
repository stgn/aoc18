import sys
from collections import Counter
from itertools import combinations


def part_one(ids):
    counts = (Counter(x).values() for x in ids)
    present = ((2 in c, 3 in c) for c in counts)
    two, three = map(sum, zip(*present))
    return two * three


def part_two(ids):
    for a, b in combinations(ids, 2):
        same = ''.join(x for x, y in zip(a, b) if x == y)
        if len(same) == len(a) - 1:
            return same


if __name__ == '__main__':
    fn, = sys.argv[1:]
    with open(fn) as f:
        ids = [x.strip() for x in f]

    print(part_one(ids))
    print(part_two(ids))
