import fileinput
import re
import numpy as np
from dataclasses import dataclass

claim_pattern = re.compile(r'#(\d+) @ (\d+),(\d+): (\d+)x(\d+)')


@dataclass(frozen=True)
class Claim:
    id_: int
    left: int
    top: int
    right: int
    bottom: int

    @classmethod
    def from_str(cls, claim_str):
        m = claim_pattern.match(claim_str)
        id_, x, y, w, h = map(int, m.groups())
        return cls(id_, x, y, x + w, y + h)


def part_one(fabric):
    return np.count_nonzero(fabric > 1)


def part_two(fabric, claims):
    for c in claims:
        patch = fabric[c.left:c.right, c.top:c.bottom]
        if (patch == 1).all():
            return c.id_


if __name__ == '__main__':
    with fileinput.input() as f:
        claims = list(map(Claim.from_str, f))

    fw = max(c.right for c in claims)
    fh = max(c.bottom for c in claims)
    fabric = np.zeros((fw, fh), dtype=np.uint16)

    for c in claims:
        fabric[c.left:c.right, c.top:c.bottom] += 1

    print(part_one(fabric))
    print(part_two(fabric, claims))
