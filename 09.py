import sys
from collections import deque


if __name__ == '__main__':
    player_count, last_marble = map(int, sys.argv[1:])

    circle = deque([0])
    scores = [0] * player_count

    for i in range(1, last_marble + 1):
        if i % 23 == 0:
            circle.rotate(7)
            bonus = circle.pop()
            scores[i % player_count] += i + bonus
            circle.rotate(-1)
        else:
            circle.rotate(-1)
            circle.append(i)

    print(max(scores))
