import fileinput
import string


def react(polymer, ignore=None):
    if ignore:
        fn = lambda x: x.lower() != ignore
        polymer = filter(fn, polymer)

    stack = []

    for x in polymer:
        if stack and x.swapcase() == stack[-1]:
            stack.pop()
        else:
            stack.append(x)

    return len(stack)


def part_two(polymer):
    return min(react(polymer, c) for c in string.ascii_lowercase)


if __name__ == '__main__':
    with fileinput.input() as f:
        polymer = f.readline().strip()

    print(react(polymer))
    print(part_two(polymer))
