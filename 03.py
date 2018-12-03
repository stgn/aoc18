import sys
import re
import numpy as np
from collections import namedtuple

pattern = re.compile(r'#(\d+) @ (\d+),(\d+): (\d+)x(\d+)')
Claim = namedtuple('Claim', ('id_', 'x1', 'y1', 'x2', 'y2'))


def parse_claim(claim_str):
    m = pattern.match(claim_str)
    id_, x, y, w, h = map(int, m.groups())
    return Claim(id_, x, y, x + w, y + h)


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
        claims = list(map(parse_claim, f))

    fw = max(c.x2 for c in claims)
    fh = max(c.y2 for c in claims)
    fabric = np.zeros((fw, fh), dtype=np.uint16)

    for c in claims:
        fabric[c.x1:c.x2, c.y1:c.y2] += 1

    print(part_one(fabric))
    print(part_two(fabric, claims))
