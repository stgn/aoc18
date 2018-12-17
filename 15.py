import fileinput
from dataclasses import dataclass
from typing import NamedTuple
from enum import IntEnum
from itertools import count, product
from collections import deque


class Vec2(NamedTuple):
    y: int
    x: int

    def __add__(self, other):
        return Vec2(x=self.x + other.x, y=self.y + other.y)

    def neighbors(self):
        return [self + a for a in Vec2.NEIGHBORS_ORDERED]


Vec2.NEIGHBORS_ORDERED = (
    Vec2(x=0, y=-1),
    Vec2(x=-1, y=0),
    Vec2(x=1, y=0),
    Vec2(x=0, y=1),
)


class Team(IntEnum):
    ELF = 0
    GOBLIN = 1


char_teams = {'E': Team.ELF, 'G': Team.GOBLIN}


@dataclass
class Unit:
    pos: Vec2
    team: Team
    hp: int = 200
    ap: int = 3

    @property
    def alive(self):
        return self.hp > 0


def find_step(walls, units, origin, targets):
    occupied = {u.pos for u in units if u.alive}
    queue = deque([origin])
    paths = {origin: None}
    found = []

    while queue:
        p = queue.popleft()

        if p in targets:
            found.append(p)

        if found:
            continue

        for n in p.neighbors():
            if n in paths or n in walls or n in occupied:
                continue
            paths[n] = p
            queue.append(n)

    if found:
        step = min(found)
        parent = paths[step]

        while parent != origin:
            step = parent
            parent = paths[parent]

        return step


if __name__ == '__main__':
    with fileinput.input() as f:
        ascii_world = list(f)

    walls = set()
    units = []

    height = len(ascii_world)
    width = max(len(x.strip()) for x in ascii_world)

    for y, x in product(range(height), range(width)):
        c = ascii_world[y][x]
        if c == '#':
            walls.add(Vec2(x=x, y=y))
        elif c in char_teams:
            units.append(Unit(Vec2(x=x, y=y), char_teams[c]))

    for r in count():
        units.sort(key=lambda u: u.pos)

        done = False

        for u in units:
            if u.hp <= 0:
                continue

            enemies = [v for v in units if u.team != v.team and v.alive]

            if not enemies:
                done = True
                break

            ignore = {v.pos for v in units if v.alive and v is not u}
            targets = {x for v in enemies for x in v.pos.neighbors()
                       if x not in walls and x not in ignore}

            if u.pos not in targets:
                step = find_step(walls, units, u.pos, targets)
                if step:
                    u.pos = step

            neighbors = u.pos.neighbors()
            attackable = [v for v in enemies if v.pos in neighbors]

            if attackable:
                enemy = min(attackable, key=lambda v: (v.hp, v.pos))
                enemy.hp -= u.ap

        units = [u for u in units if u.alive]

        if done:
            break

    total_hp = sum(u.hp for u in units)
    print(r * total_hp)
