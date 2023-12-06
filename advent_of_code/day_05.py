from collections import defaultdict
import re
from typing import Callable, Mapping, TypeAlias

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


def trails(input: str) -> tuple[Paths, SeedMappings]:
    """Find the paths and the seed mappings from the input text."""
    _seeds, _, maps = input.split("\n", maxsplit=2)

    paths = ["seed"]
    almanac: Mapping[tuple[str, str], list[Callable[[int], int | None]]] = defaultdict(
        list
    )

    for m in MAPS.finditer(maps):
        src_name, dest_name, _ranges = m.groups()
        paths.append(dest_name)
        for ranges in _ranges.splitlines():
            fn = converter_factory(*map(int, DIGIT.findall(ranges)))

            almanac[(src_name, dest_name)].append(fn)
    seeds = tuple(map(int, DIGIT.findall(_seeds)))
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


def main():
    with utils.contents() as contents:
        print("Part one:", lowest_location(contents, "location"))


if __name__ == "__main__":
    main()
