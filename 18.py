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


def simulate(init_state, generations):
    seen = {}
    cached_counts = []
    state = init_state
    offset = 0

    for g in range(1, generations + 1):
        new_state = [0] * (50 * 50)

        for y, x in product(range(50), range(50)):
            adj = ((y - 1, x - 1), (y - 1, x), (y - 1, x + 1),
                   (y, x - 1), (y, x + 1),
                   (y + 1, x - 1), (y + 1, x), (y + 1, x + 1))
            cur = state[y * 50 + x]
            adj_count = Counter(get_cell(state, *n) for n in adj)

            new = cur
            num_trees = adj_count[Cell.TREES]
            num_yards = adj_count[Cell.YARD]

            if cur == Cell.OPEN and num_trees >= 3:
                new = Cell.TREES

            if cur == Cell.TREES and num_yards >= 3:
                new = Cell.YARD

            if cur == Cell.YARD and 0 in (num_yards, num_trees):
                new = Cell.OPEN

            new_state[y * 50 + x] = new

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

    print(simulate(state, 10))
    print(simulate(state, 1_000_000_000))
