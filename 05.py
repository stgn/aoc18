import fileinput
import string


def react(polymer, ignore=None):
    if ignore:
        ignore = ord(ignore)

    stack = []

    for u in map(ord, polymer):
        if u | 32 == ignore:  # u.lower()
            continue

        annihilate = False
        if stack:
            top = stack[-1]
            annihilate = u ^ 32 == top  # u.swapcase()

        if annihilate:
            stack.pop()
        else:
            stack.append(u)

    return len(stack)


def part_two(polymer):
    return min(react(polymer, c) for c in string.ascii_lowercase)


if __name__ == '__main__':
    with fileinput.input() as f:
        polymer = f.readline().strip()

    print(react(polymer))
    print(part_two(polymer))
