import fileinput
import heapq
from collections import defaultdict


def toporder(adjacency):
    indegree = defaultdict(int)
    for u, adjacents in adjacency.items():
        indegree[u]
        for v in adjacents:
            indegree[v] += 1
    
    queue = [u for u, d in indegree.items() if not d]
    heapq.heapify(queue)

    while queue or sum(indegree.values()):
        u = yield heapq.heappop(queue) if queue else None
        if not u:
            continue
        for v in adjacency[u]:
            indegree[v] -= 1
            if not indegree[v]:
                heapq.heappush(queue, v)


def topsort(rules):
    g = toporder(rules)
    last = None
    while True:
        try:
            last = g.send(last)
            yield last
        except StopIteration:
            break


def part_one(rules):
    return ''.join(topsort(rules))


def part_two(rules):
    scheduler = toporder(rules)
    more_tasks = True
    workers = [(None, 0)] * 5
    notify = []
    time = 0

    while True:
        for i, (task, eta) in enumerate(workers):
            if not task or time < eta:
                continue
            notify.append(task)
            workers[i] = None, 0

        if more_tasks:
            for i, (task, _) in enumerate(workers):
                if task:
                    continue
                try:
                    completed_task = notify.pop() if notify else None
                    new_task = scheduler.send(completed_task)
                    if not new_task:
                        break
                    eta = time + ord(new_task) - 64 + 60
                    workers[i] = new_task, eta
                except StopIteration:
                    more_tasks = False
                    break
        elif all(not task for task, _ in workers):
            break

        time += 1

    return time


if __name__ == '__main__':
    rules = defaultdict(list)

    with fileinput.input() as f:
        for l in f:
            step, requires = l[5], l[36]
            rules[step].append(requires)

    print(part_one(rules))
    print(part_two(rules))