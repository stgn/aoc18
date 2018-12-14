import fileinput
import numpy as np
from dataclasses import dataclass
from enum import IntEnum


@dataclass(frozen=True, eq=True)
class Vec2:
    x: int = 0
    y: int = 0

    def __add__(self, other):
        return Vec2(self.x + other.x, self.y + other.y)

    def __str__(self):
        return f'{self.x},{self.y}'


@dataclass
class Cart:
    pos: Vec2
    vel: Vec2
    turn_step: int = 0
    crashed: bool = False

    def move_forward(self):
        self.pos += self.vel

    def turn_left(self):
        self.vel = Vec2(self.vel.y, -self.vel.x)

    def turn_right(self):
        self.vel = Vec2(-self.vel.y, self.vel.x)


class Path(IntEnum):
    INTERSECTION = 1
    DIAGONAL = 2
    ANTIDIAGONAL = 3


char_direction = {
    '^': Vec2(0, -1),
    '>': Vec2(1, 0),
    'v': Vec2(0, 1),
    '<': Vec2(-1, 0)
}


char_segment = {
    '\\': Path.DIAGONAL,
    '/': Path.ANTIDIAGONAL,
    '+': Path.INTERSECTION
}


if __name__ == '__main__':
    with fileinput.input() as f:
        ascii_net = [x.rstrip('\n') for x in f]

    height, width = len(ascii_net), max(map(len, ascii_net))
    net = np.empty((height, width), np.uint8)
    carts = []

    for y, x in np.ndindex((height, width)):
        c = ascii_net[y][x]
        net[y, x] = char_segment.get(c, 0)

        if c in char_direction:
            pos = Vec2(x, y)
            vel = char_direction[c]
            carts.append(Cart(pos, vel))

    first_crash = None

    while len(carts) > 1:
        for c in carts:
            if c.crashed:
                continue

            c.move_forward()

            for co in carts:
                if c is co:
                    continue
                if c.pos == co.pos:
                    first_crash = first_crash or c.pos
                    c.crashed = co.crashed = True
                    break

            segment = net[c.pos.y, c.pos.x]

            if not c.crashed and segment:
                if segment == Path.INTERSECTION:
                    if c.turn_step == 0:
                        c.turn_left()
                    elif c.turn_step == 2:
                        c.turn_right()
                    c.turn_step = (c.turn_step + 1) % 3
                else:
                    is_anti = segment == Path.ANTIDIAGONAL
                    is_vertical = c.vel.x == 0
                    if is_anti ^ is_vertical:
                        c.turn_left()
                    else:
                        c.turn_right()

        carts = [c for c in carts if not c.crashed]
        carts.sort(key=lambda c: (c.pos.y, c.pos.x))

    print(first_crash)
    print(carts[0].pos)
