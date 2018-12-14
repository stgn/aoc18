import sys


def subseq_index(haystack, needle):
    needle_len = len(needle)
    for x in range(len(haystack) - needle_len + 1):
        if haystack[x:x + needle_len] == needle:
            return x


if __name__ == '__main__':
    puzzle_input = sys.argv[1]
    count = int(puzzle_input)
    target = list(map(int, puzzle_input))

    scores = [3, 7]
    elves = [0, 1]
    part_one = None

    while len(scores) < 100_000_000:
        elf_scores = [scores[e] for e in elves]
        scores.extend(map(int, str(sum(elf_scores))))

        if part_one is None and len(scores) >= count + 10:
            part_one = scores[count:count + 10]
            print(''.join(map(str, part_one)))

        check = scores[-7:]
        idx = subseq_index(check, target)
        if idx is not None:
            print(len(scores) - 7 + idx)
            break

        elves = [(e + s + 1) % len(scores)
                 for e, s in zip(elves, elf_scores)]
