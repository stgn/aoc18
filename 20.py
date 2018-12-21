import fileinput
from collections import defaultdict, deque
from typing import NamedTuple


class Vec2(NamedTuple):
    x: int = 0
    y: int = 0

    def __add__(self, other):
        return Vec2(self.x + other.x, self.y + other.y)


class PathNode(NamedTuple):
    distance: int
    parent: Vec2


Vec2.CARDINAL = {
    'N': Vec2(0, -1),
    'E': Vec2(1, 0),
    'S': Vec2(0, 1),
    'W': Vec2(-1, 0),
}


def part_one(paths):
    return max(pn.distance for pn in paths.values())


def part_two(paths):
    return sum(pn.distance >= 1000 for pn in paths.values())


if __name__ == '__main__':
    with fileinput.input() as f:
        expr = next(f).strip()[1:-1]

    origin = Vec2()
    edges = defaultdict(set)

    stack = []
    pos = {origin}
    splits = ends = None

    for c in expr:
        if c in 'NESW':
            d = Vec2.CARDINAL[c]
            for p in pos:
                edges[p].add(p + d)
            pos = {p + d for p in pos}
        elif c == '(':
            stack.append((splits, ends))
            splits, ends = pos, set()
        elif c == '|':
            ends |= pos
            pos = splits
        elif c == ')':
            pos |= ends
            splits, ends = stack.pop()

    paths = {origin: PathNode(0, None)}
    queue = deque([(0, origin)])

    while queue:
        d, p = queue.popleft()
        for n in edges[p]:
            if n in paths:
                continue
            paths[n] = PathNode(d + 1, p)
            queue.append((d + 1, n))

    print(part_one(paths))
    print(part_two(paths))
