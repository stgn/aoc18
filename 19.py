import fileinput
import operator
from enum import IntEnum


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


if __name__ == '__main__':
    with fileinput.input() as f:
        ip_reg = int(next(f)[4:])
        program = [x.split() for x in f]

    ip = 0
    regs = [0] * 6

    while ip < len(program):
        fetched = program[ip]
        regs[ip_reg] = ip
        op = fetched[0]
        operands = tuple(map(int, fetched[1:]))
        do_op(op_table[op], regs, operands)
        ip = regs[ip_reg] + 1

    print(regs[0])
