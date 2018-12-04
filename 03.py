import sys
import re
import numpy as np
from dataclasses import dataclass

claim_pattern = re.compile(r'#(\d+) @ (\d+),(\d+): (\d+)x(\d+)')


@dataclass(frozen=True)
class Claim:
    id_: int
    x1: int; y1: int
    x2: int; y2: int

    @classmethod
    def from_str(cls, claim_str):
        m = claim_pattern.match(claim_str)
        id_, x, y, w, h = map(int, m.groups())
        return cls(id_, x, y, x + w, y + h)


def part_one(fabric):
    return np.count_nonzero(fabric > 1)


def part_two(fabric, claims):
    for c in claims:
        patch = fabric[c.x1:c.x2, c.y1:c.y2]
        if (patch == 1).all():
            return c.id_


if __name__ == '__main__':
    fn, = sys.argv[1:]
    with open(fn) as f:
        claims = list(map(Claim.from_str, f))

    fw = max(c.x2 for c in claims)
    fh = max(c.y2 for c in claims)
    fabric = np.zeros((fw, fh), dtype=np.uint16)

    for c in claims:
        fabric[c.x1:c.x2, c.y1:c.y2] += 1

    print(part_one(fabric))
    print(part_two(fabric, claims))
