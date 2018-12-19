import fileinput
from enum import IntEnum
from collections import Counter
from itertools import product


class Cell(IntEnum):
    OPEN = 0
    TREES = 1
    YARD = 2


def get_cell(state, y, x):
    if 0 <= x < 50 and 0 <= y < 50:
        return state[y * 50 + x]
    return Cell.OPEN


def precalc_rules():
    rules = {}

    for neighborhood in product(Cell, repeat=9):
        center = neighborhood[4]
        count = Counter(neighborhood)
        count[center] -= 1
        num_trees = count[Cell.TREES]
        num_yards = count[Cell.YARD]

        if center == Cell.OPEN and num_trees >= 3:
            rules[neighborhood] = Cell.TREES

        if center == Cell.TREES and num_yards >= 3:
            rules[neighborhood] = Cell.YARD

        if center == Cell.YARD and 0 in (num_yards, num_trees):
            rules[neighborhood] = Cell.OPEN

    return rules


def simulate(rules, init_state, generations):
    seen = {}
    cached_counts = []
    state = init_state
    offset = 0

    for g in range(1, generations + 1):
        new_state = [0] * (50 * 50)

        for y, x in product(range(50), range(50)):
            adj = ((y - 1, x - 1), (y - 1, x), (y - 1, x + 1),
                   (y,     x - 1), (y,     x), (y,     x + 1),
                   (y + 1, x - 1), (y + 1, x), (y + 1, x + 1))
            neighborhood = tuple(get_cell(state, *n) for n in adj)
            center = neighborhood[4]
            new_state[y * 50 + x] = rules.get(neighborhood, center)

        state = tuple(new_state)

        if state in seen:
            period = g - seen[state]
            offset = period - (generations - g) % period
            break

        seen[state] = g
        cached_counts.append(Counter(state))

    total_count = cached_counts[g - offset - 1]
    return total_count[Cell.TREES] * total_count[Cell.YARD]


if __name__ == '__main__':
    with fileinput.input() as f:
        lines = list(f)

    state = [0] * (50 * 50)
    for y, x in product(range(50), range(50)):
        ch = lines[y][x]
        if ch != '.':
            cell = Cell.YARD if ch == '#' else Cell.TREES
            state[y * 50 + x] = cell

    rules = precalc_rules()

    print(simulate(rules, state, 10))
    print(simulate(rules, state, 1_000_000_000))
