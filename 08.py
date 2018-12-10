import fileinput
from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class Node:
    children: List['Node']
    metadata: List[int]
    meta_sum: int

    @classmethod
    def parse_from(cls, s):
        nc, nm = next(s), next(s)
        children = [cls.parse_from(s) for _ in range(nc)]
        metadata = [next(s) for _ in range(nm)]
        meta_sum = sum(metadata)
        return cls(children, metadata, meta_sum)


def part_one(node):
    child_sums = sum(part_one(c) for c in node.children)
    return child_sums + node.meta_sum


def part_two(node):
    c = node.children
    if not c:
        return node.meta_sum
    return sum(part_two(c[i - 1]) for i in node.metadata if i <= len(c))


if __name__ == '__main__':
    with fileinput.input() as f:
        line = f.readline()
        data = map(int, line.split())
        node = Node.parse_from(data)

    print(part_one(node))
    print(part_two(node))
