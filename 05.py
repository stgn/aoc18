import fileinput
import string


def react(polymer):
    stack = []
    for x in polymer:
        if stack and x.swapcase() == stack[-1]:
            stack.pop()
        else:
            stack.append(x)
    return len(stack)


def make_unit_filter(unit):
    return lambda x: x.lower() != unit


def part_two(polymer):
    filters = map(make_unit_filter, string.ascii_lowercase)
    polymers = (filter(f, polymer) for f in filters)
    return min(react(p) for p in polymers)


if __name__ == '__main__':
    with fileinput.input() as f:
        polymer = f.readline().strip()

    print(react(polymer))
    print(part_two(polymer))
