import fileinput
import operator
from ast import literal_eval
from collections import defaultdict
from enum import IntEnum
from functools import partial


class Operand(IntEnum):
    ZERO = 0
    IMM = 1
    REG = 2


op_table = {
    'addr': (operator.add,  Operand.REG, Operand.REG),
    'addi': (operator.add,  Operand.REG, Operand.IMM),
    'mulr': (operator.mul,  Operand.REG, Operand.REG),
    'muli': (operator.mul,  Operand.REG, Operand.IMM),
    'banr': (operator.and_, Operand.REG, Operand.REG),
    'bani': (operator.and_, Operand.REG, Operand.IMM),
    'borr': (operator.or_,  Operand.REG, Operand.REG),
    'bori': (operator.or_,  Operand.REG, Operand.IMM),
    'setr': (operator.add,  Operand.REG, Operand.ZERO),
    'seti': (operator.add,  Operand.IMM, Operand.ZERO),
    'gtir': (operator.gt,   Operand.IMM, Operand.REG),
    'gtri': (operator.gt,   Operand.REG, Operand.IMM),
    'gtrr': (operator.gt,   Operand.REG, Operand.REG),
    'eqir': (operator.eq,   Operand.IMM, Operand.REG),
    'eqri': (operator.eq,   Operand.REG, Operand.IMM),
    'eqrr': (operator.eq,   Operand.REG, Operand.REG),
}


operand_getter = {
    Operand.ZERO: lambda *_: 0,
    Operand.IMM: lambda o, _: o,
    Operand.REG: lambda o, s: s[o]
}


def do_op(op, state, operands):
    base_op, atype, btype = op
    a = operand_getter[atype](operands[0], state)
    b = operand_getter[btype](operands[1], state)
    c = operands[2]
    state[c] = int(base_op(a, b))


def parse_sample(it):
    before = next(it)
    if not before.strip():
        return
    before = literal_eval(before[8:])
    instr = list(map(int, next(it).split()))
    after = literal_eval(next(it)[8:])
    return instr, before, after


if __name__ == '__main__':
    samples = []

    with fileinput.input() as f:
        while True:
            parsed = parse_sample(f)
            if not parsed:
                break
            samples.append(parsed)
            next(f)
        next(f)
        program = [list(map(int, x.split())) for x in f]

    acts_like = defaultdict(lambda: set(op_table))
    acts_like_three_or_more = 0

    for instr, before, after in samples:
        candidates = set()
        opcode, *operands = instr

        for mnemonic, op in op_table.items():
            state = before[:]
            do_op(op, state, operands)
            if state == after:
                candidates.add(mnemonic)

        acts_like[opcode] &= candidates

        if len(candidates) >= 3:
            acts_like_three_or_more += 1

    op_dispatch = {}
    while len(op_dispatch) < 16:
        opcode, candidates = next((k, v) for k, v in acts_like.items()
                                  if len(v) == 1)
        mnemonic = candidates.pop()
        op_dispatch[opcode] = partial(do_op, op_table[mnemonic])
        for c in acts_like.values():
            c.discard(mnemonic)

    state = [0] * 4
    for opcode, *operands in program:
        op_dispatch[opcode](state, operands)

    print(acts_like_three_or_more)
    print(state[0])
