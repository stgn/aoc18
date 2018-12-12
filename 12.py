import fileinput


def simulate(rules, init_state, generations):
    old_state = init_state
    origin = 0

    for g in range(1, generations + 1):
        state = f'....{old_state}....'
        state = ''.join(rules.get(state[x:x + 5], '.')
                        for x in range(len(state) - 4))

        left = state.index('#')
        right = state.rindex('#') + 1
        state = state[left:right]

        origin -= left - 2

        if state == old_state:
            origin -= (generations - g) * (left - 2)
            break

        old_state = state

    return sum(i - origin for i, x in enumerate(state) if x == '#')


if __name__ == '__main__':
    with fileinput.input() as f:
        state = f.readline()[15:].strip()
        next(f)
        rules = {x[:5]: x[9] for x in f}

    print(simulate(rules, state, 20))
    print(simulate(rules, state, 50_000_000_000))
