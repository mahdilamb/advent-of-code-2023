import functools
import math
import re
from typing import Callable, NamedTuple, Sequence
import advent_of_code.utils as utils

DIGIT = re.compile(r"\d+")


class RaceRecords(NamedTuple):
    """Named tuple containing the race records."""

    time: int
    distance: int


def parse_input(input: str) -> Sequence[RaceRecords]:
    """Parse the input into records."""
    return tuple(
        RaceRecords(time, distance)
        for time, distance in zip(
            *map(
                lambda line: tuple(map(int, DIGIT.findall(line))),
                input.splitlines(),
            )
        )
    )


def race(held_for: int, duration: int):
    """Calculate the distance traveled in the first race."""
    moved_for = duration - held_for
    return moved_for * held_for


def race_combos(*, race_duration: int, record_distance: int) -> Sequence[int]:
    """Get the race combos for specific race."""
    race_fn = functools.partial(race, duration=race_duration)
    return tuple(
        held_for
        for held_for in range(race_duration)
        if race_fn(held_for) > record_distance
    )


def parse_input_to_race_combos(input: str) -> Sequence[Sequence[int]]:
    """Parse input into the race combos."""
    return tuple(
        race_combos(race_duration=race.time, record_distance=race.distance)
        for race in parse_input(input)
    )


first_race_combos = functools.partial(race_combos, race_duration=7, record_distance=9)
second_race_combos = functools.partial(
    race_combos, race_duration=15, record_distance=40
)
third_race_combos = functools.partial(
    race_combos, race_duration=30, record_distance=200
)


def margin_of_error(*races: Sequence[int]):
    """Calculate margin of error from multiple races."""
    return math.prod(tuple(len(race) for race in races))


def main():
    with utils.contents() as contents:
        print("Day 2", margin_of_error(*parse_input_to_race_combos(contents)))


if __name__ == "__main__":
    main()