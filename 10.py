import fileinput
import re
import numpy as np
from dataclasses import dataclass

point_pattern = re.compile(r'position=< *(-?\d+), +(-?\d+)> '
                           r'velocity=< *(-?\d+), +(-?\d+)>')


@dataclass
class Point:
    px: int
    py: int
    vx: int
    vy: int

    @classmethod
    def from_string(cls, string):
        m = point_pattern.match(string)
        return cls(*map(int, m.groups()))


def part_one(pts):
    canvas = np.zeros((10, 62), dtype=np.uint8)

    top = min(p.py for p in pts)
    left = min(p.px for p in pts)
    for p in pts:
        canvas[p.py - top, p.px - left] = 1

    return '\n'.join(''.join(' █'[x] for x in row) for row in canvas)


if __name__ == '__main__':
    with fileinput.input() as f:
        pts = list(map(Point.from_string, f))

    top = min(p.py for p in pts)
    bottom = max(p.py for p in pts)
    rising = min(p.vy for p in pts)
    falling = max(p.vy for p in pts)

    dt = (bottom - top - 9) // (falling - rising)

    for p in pts:
        p.px += p.vx * dt
        p.py += p.vy * dt

    print(part_one(pts))
    print(dt)
