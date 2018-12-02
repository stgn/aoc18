import sys
from itertools import cycle


def part_two(deltas):
    cur = 0
    seen = set()
    for n in cycle(deltas):
        if cur in seen:
            return cur
        seen.add(cur)
        cur += n


if __name__ == '__main__':
    fn, = sys.argv[1:]
    with open(fn) as f:
        deltas = [int(x) for x in f]

    print(sum(deltas))
    print(part_two(deltas))
