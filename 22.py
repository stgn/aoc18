import sys
import heapq
from typing import NamedTuple
from enum import IntEnum
from itertools import product
from functools import lru_cache


class Vec2(NamedTuple):
    x: int = 0
    y: int = 0

    def __add__(self, other):
        return Vec2(self.x + other.x, self.y + other.y)

    def neighbors(self):
        return [self + a for a in Vec2.NEIGHBORS_ORDERED]


Vec2.NEIGHBORS_ORDERED = (
    Vec2(x=0, y=-1),
    Vec2(x=-1, y=0),
    Vec2(x=1, y=0),
    Vec2(x=0, y=1),
)


ORIGIN = Vec2()


class Region(IntEnum):
    ROCKY = 0
    WET = 1
    NARROW = 2


class Equip(IntEnum):
    NONE = 0
    TORCH = 1
    CLIMBING = 2


region_tools = {
    Region.ROCKY: (Equip.TORCH, Equip.CLIMBING),
    Region.WET: (Equip.NONE, Equip.CLIMBING),
    Region.NARROW: (Equip.NONE, Equip.TORCH)
}


class Cave:
    def __init__(self, depth, target):
        self.depth = depth
        self.target = target

    @lru_cache(maxsize=None)
    def geologic_index(self, p):
        res = 0
        if p not in (ORIGIN, self.target):
            if p.x == 0:
                res = p.y * 48271
            elif p.y == 0:
                res = p.x * 16807
            else:
                left = self.erosion_level(Vec2(p.x - 1, p.y))
                top = self.erosion_level(Vec2(p.x, p.y - 1))
                res = left * top
        return res

    @lru_cache(maxsize=None)
    def erosion_level(self, p):
        return (self.geologic_index(p) + self.depth) % 20183

    def region_type(self, p):
        return Region(self.erosion_level(p) % 3)


def part_one(cave, target):
    it = product(range(target.y + 1), range(target.x + 1))
    return sum(cave.region_type(Vec2(x, y)) for y, x in it)


def part_two(cave, target):
    q = [(0, ORIGIN, Equip.TORCH)]
    seen = set()

    while q:
        d, u, t = heapq.heappop(q)

        if u == target:
            return d + 7 * (t != Equip.TORCH)

        if (u, t) in seen:
            continue

        seen.add((u, t))

        u_tools = region_tools[cave.region_type(u)]
        switch = next(x for x in u_tools if x != t)
        heapq.heappush(q, (d + 7, u, switch))

        for v in u.neighbors():
            if v.x < 0 or v.y < 0:
                continue
            v_tools = region_tools[cave.region_type(v)]
            if t in v_tools:
                heapq.heappush(q, (d + 1, v, t))


if __name__ == '__main__':
    depth, target = sys.argv[1:]
    depth = int(depth)
    target = Vec2(*map(int, target.split(',')))

    cave = Cave(depth, target)

    print(part_one(cave, target))
    print(part_two(cave, target))
