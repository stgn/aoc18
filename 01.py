import fileinput
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
    with fileinput.input() as f:
        deltas = list(map(int, f))

    print(sum(deltas))
    print(part_two(deltas))
