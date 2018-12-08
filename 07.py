import fileinput
import heapq
from collections import defaultdict
from dataclasses import dataclass


class Scheduler:
    def __init__(self, rules):
        self.rules = rules

        self.prereqs = defaultdict(int)
        for step, dependents in rules.items():
            self.prereqs[step]
            for d in dependents:
                self.prereqs[d] += 1

        self.queue = [s for s, c in self.prereqs.items() if not c]
        heapq.heapify(self.queue)

    def get(self):
        if self.queue:
            return heapq.heappop(self.queue)

    def complete(self, step):
        if not step:
            return
        for d in self.rules[step]:
            self.prereqs[d] -= 1
            if not self.prereqs[d]:
                heapq.heappush(self.queue, d)

    def has_work(self):
        return bool(self.queue)

    def exhausted(self):
        return all(x == 0 for x in self.prereqs.values())


@dataclass(frozen=True, order=True)
class Task:
    eta: int
    step: str


def part_one(rules):
    ordered = []
    scheduler = Scheduler(rules)
    while scheduler.has_work():
        step = scheduler.get()
        ordered.append(step)
        scheduler.complete(step)
    return ''.join(ordered)


def part_two(rules, max_tasks=5):
    scheduler = Scheduler(rules)
    tasks = []

    time = 0
    while True:
        while tasks and time >= tasks[0].eta:
            t = heapq.heappop(tasks)
            scheduler.complete(t.step)

        if scheduler.has_work():
            while len(tasks) < max_tasks:
                new_step = scheduler.get()
                if new_step is None:
                    break
                eta = time + ord(new_step) - 64 + 60
                heapq.heappush(tasks, Task(eta, new_step))
        elif scheduler.exhausted():
            return time

        time = tasks[0].eta


if __name__ == '__main__':
    rules = defaultdict(list)

    with fileinput.input() as f:
        for l in f:
            step, requires = l[5], l[36]
            rules[step].append(requires)

    print(part_one(rules))
    print(part_two(rules))
