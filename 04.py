import sys
import re
import numpy as np
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime

record_pattern = re.compile(r'\[(\d+-\d+-\d+ \d+:\d+)\] (.+)')
switch_pattern = re.compile(r'Guard #(?P<new_guard_id>\d+) begins shift')


@dataclass(frozen=True, order=True)
class Record:
    timestamp: datetime
    action: str

    @classmethod
    def from_str(cls, record_str):
        m = record_pattern.match(record_str)
        ts_str, action = m.groups()
        return cls(datetime.fromisoformat(ts_str), action)


@dataclass(frozen=True)
class Stats:
    spent_asleep: int
    mostly_at: int
    mostly_observations: int

    @classmethod
    def from_schedule(cls, schedule):
        spent_asleep = np.sum(schedule)
        mostly_at = np.argmax(schedule)
        mostly_observations = schedule[mostly_at]
        return cls(spent_asleep, mostly_at, mostly_observations)


def part_one(stats):
    guard_id = max(stats, key=lambda k: stats[k].spent_asleep)
    return guard_id * stats[guard_id].mostly_at


def part_two(stats):
    guard_id = max(stats, key=lambda k: stats[k].mostly_observations)
    return guard_id * stats[guard_id].mostly_at


if __name__ == '__main__':
    fn, = sys.argv[1:]
    with open(fn) as f:
        records = sorted(map(Record.from_str, f))

    schedules = defaultdict(lambda: np.zeros(60, dtype=np.uint8))
    guard_id, sleep_began = None, None
    for r in records:
        minute = r.timestamp.minute 
        switch = switch_pattern.match(r.action)

        if switch:
            guard_id = int(switch['new_guard_id'])
        elif r.action == 'falls asleep':
            sleep_began = minute
        elif r.action == 'wakes up':
            schedule = schedules[guard_id]
            schedule[sleep_began:minute] += 1

    stats = {k: Stats.from_schedule(v) for k, v in schedules.items()}
    print(part_one(stats))
    print(part_two(stats))
