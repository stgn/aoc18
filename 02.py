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


def part_two_alt(ids):
    min_len = min(map(len, ids))
    for i in range(min_len):
        seen = set()
        for x in ids:
            spliced = x[:i] + x[i + 1:]
            if spliced in seen:
                return spliced
            seen.add(spliced)


if __name__ == '__main__':
    fn, = sys.argv[1:]
    with open(fn) as f:
        ids = [x.strip() for x in f]

    print(part_one(ids))
    print(part_two_alt(ids))
