import sys
import fileinput
import re
from enum import IntEnum, auto

line_pattern = re.compile(r'([xy])=(\d+), [xy]=(\d+)..(\d+)')


class Axis(IntEnum):
    X = auto()
    Y = auto()


def parse_line(string):
    m = line_pattern.match(string.strip())
    fixed, *coords = m.groups()
    fixed = Axis.X if fixed == 'x' else Axis.Y
    return (fixed, *map(int, coords))


def flow(clay, bottom):
    still, moving = set(), set()

    def traverse(p):
        if p in moving:
            return False

        moving.add(p)

        x, y = p

        if y >= bottom:
            return False

        below = (x, y + 1)

        if below not in clay:
            traverse(below)

        if below not in clay and below not in still:
            return False

        left = (x - 1, y)
        right = (x + 1, y)

        left_finite = left in clay or traverse(left)
        right_finite = right in clay or traverse(right)

        if left_finite and right_finite:
            still.add(p)
            while left in moving:
                still.add(left)
                left = (left[0] - 1, y)
            while right in moving:
                still.add(right)
                right = (right[0] + 1, y)

        return left_finite or right_finite

    traverse((500, 0))
    return still, moving


if __name__ == '__main__':
    sys.setrecursionlimit(9001)

    with fileinput.input() as f:
        lines = list(map(parse_line, f))

    clay = set()

    top = min(a if o == Axis.Y else b for o, a, b, _ in lines)
    bottom = max(a if o == Axis.Y else c for o, a, _, c in lines)

    for o, a, b, c in lines:
        for x in range(b, c + 1):
            if o == Axis.Y:
                p = (x, a)
            else:
                p = (a, x)
            clay.add(p)

    still, moving = flow(clay, bottom)

    print(sum(top <= y <= bottom for x, y in still | moving))
    print(sum(top <= y <= bottom for x, y in still))
