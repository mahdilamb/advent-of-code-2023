from collections import defaultdict
from collections.abc import Iterator
import re
from typing import Callable, Mapping, NamedTuple, Optional, TypeAlias, Union

from advent_of_code import utils

Paths: TypeAlias = tuple[str, ...]
SeedMappings: TypeAlias = dict[int, tuple[int, ...]]
MAPS = re.compile(r"^(\w+)-to-(\w+) map:\n([\s\S]+?)(?:^$|\Z)", re.M)
DIGIT = re.compile(r"\d+")


def converter_factory(
    dest_start: int, src_start: int, range_length: int
) -> Callable[[int], int | None]:
    """Create a converter that uses the range information."""
    max_src = src_start + range_length
    diff = dest_start - src_start

    def converter(x: int) -> int | None:
        if src_start <= x < max_src:
            return diff + x
        return None

    return converter


def read_input(input: str):
    _seeds, _, maps = input.split("\n", maxsplit=2)

    paths = ["seed"]
    almanac: Mapping[tuple[str, str], list[tuple[int, int, int]]] = defaultdict(list)

    for m in MAPS.finditer(maps):
        src_name, dest_name, _ranges = m.groups()
        paths.append(dest_name)
        for ranges in _ranges.splitlines():
            almanac[(src_name, dest_name)].append(
                tuple(map(int, DIGIT.findall(ranges)))
            )
    seeds = tuple(map(int, DIGIT.findall(_seeds)))
    return seeds, paths, dict(almanac)


def trails(input: str) -> tuple[Paths, SeedMappings]:
    """Find the paths and the seed mappings from the input text."""
    seeds, paths, _almanac = read_input(input)
    almanac: Mapping[tuple[str, str], list[Callable[[int], int | None]]] = {
        k: [converter_factory(*w) for w in v] for k, v in _almanac.items()
    }
    mapped: SeedMappings = {}
    for seed in seeds:
        path = [seed]
        for src, dest in zip(paths[:-1], paths[1:]):
            val = path[-1]
            for converter in almanac[(src, dest)]:
                next_val = converter(val)
                if next_val is not None:
                    path.append(next_val)
                    break
            else:
                path.append(val)
        mapped[seed] = tuple(path)
    return tuple(paths), mapped


def lowest_location(input: str, loc: str) -> int:
    """Find the lower location at a specific position."""
    paths, mappings = trails(input)
    i = paths.index(loc)
    return min(mapping[i] for mapping in mappings.values())


def ranged_trails(input: str):
    _seeds, paths, _almanac = read_input(input)

    seeds = tuple(
        (start, start + length - 1) for start, length in zip(_seeds[0::2], _seeds[1::2])
    )
    almanac: Mapping[tuple[str, str], list[Callable[[int], int | None]]] = {
        k: [converter_factory(*w) for w in v] for k, v in _almanac.items()
    }
    mapped = {}
    for seed in seeds:
        print(seed)
        path = [seed]
        for src, dest in zip(paths[:-1], paths[1:]):
            val = path[-1]
            for converter in almanac[(src, dest)]:
                next_val = tuple(map(converter, val))
                if None not in next_val:
                    path.append(next_val)
                    break
            else:
                path.append(val)
        mapped[seed] = tuple(path)
    return tuple(paths), mapped


def lowest_ranged_location(input: str, loc: str) -> int:
    """Find the lower location at a specific position."""
    paths, mappings = ranged_trails(input)
    i = paths.index(loc)
    return min(mapping[i][0] for mapping in mappings.values())


print(
    lowest_ranged_location(
        r"""seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4""",
        "location",
    )
)
exit()


def main():
    with utils.contents() as contents:
        print("Part one:", lowest_location(contents, "location"))


if __name__ == "__main__":
    main()
