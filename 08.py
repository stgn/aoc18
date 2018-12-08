import fileinput
from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class Node:
    children: List['Node']
    metadata: List[int]

    @classmethod
    def parse_from(cls, s):
        nc, nm = next(s), next(s)
        children = [cls.parse_from(s) for _ in range(nc)]
        metadata = [next(s) for _ in range(nm)]
        return cls(children, metadata)


def part_one(node):
    child_sums = sum(part_one(c) for c in node.children)
    meta_sum = sum(node.metadata)
    return child_sums + meta_sum


def part_two(node):
    c, m = node.children, node.metadata
    return sum(part_two(c[i - 1]) for i in m if i <= len(c)) if c else sum(m)


if __name__ == '__main__':
    with fileinput.input() as f:
        line = f.readline()
        data = map(int, line.split())
        node = Node.parse_from(data) 

    print(part_one(node))
    print(part_two(node))
