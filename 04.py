import sys
import re
import numpy as np
from collections import defaultdict, namedtuple
from operator import attrgetter

Stats = namedtuple('Stats', ('guard_id', 'spent_asleep', 
                             'mostly_at', 'mostly_value'))
record_pattern = re.compile(r'\[(\d+)-(\d+)-(\d+) (\d+):(\d+)\] (.+)')
switch_pattern = re.compile(r'Guard #(\d+) begins shift')


def parse_record(record_str):
    m = record_pattern.match(record_str)
    *time, action = m.groups()
    return tuple(map(int, time)), action


def get_stats(item):
    guard_id, schedule = item
    spent_asleep = np.sum(schedule)
    mostly_at = np.argmax(schedule)
    mostly_value = schedule[mostly_at]
    return Stats(guard_id, spent_asleep, mostly_at, mostly_value)


def part_one(stats):
    x = max(stats, key=attrgetter('spent_asleep'))
    return x.guard_id * x.mostly_at


def part_two(stats):
    x = max(stats, key=attrgetter('mostly_value'))
    return x.guard_id * x.mostly_at


if __name__ == '__main__':
    fn, = sys.argv[1:]
    with open(fn) as f:
        records = sorted(map(parse_record, f))

    schedules = defaultdict(lambda: np.zeros(60, dtype=np.uint8))
    guard_id, sleep_began = None, None
    for time, action in records:
        *_, minute = time 
        switch = switch_pattern.match(action)

        if switch:
            guard_id = int(switch[1])
        elif action == 'falls asleep':
            sleep_began = minute
        elif action == 'wakes up':
            schedule = schedules[guard_id]
            schedule[sleep_began:minute] += 1

    stats = list(map(get_stats, schedules.items()))
    print(part_one(stats))
    print(part_two(stats))
