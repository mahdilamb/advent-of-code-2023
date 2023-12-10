"""Code for day 5."""
import bisect
from collections import defaultdict
import re
from typing import Callable, Mapping, NamedTuple, Sequence, TypeAlias

from advent_of_code import utils

Paths: TypeAlias = tuple[str, ...]
ItemizedSeedMappings: TypeAlias = dict[int, tuple[int, ...]]
MAPS = re.compile(r"^(\w+)-to-(\w+) map:\n([\s\S]+?)(?:^$|\Z)", re.M)
DIGIT = re.compile(r"\d+")


class AlmanacRow(NamedTuple):
    """Data storage for a row used in the almanac."""

    dest_start: int
    src_start: int
    range_length: int

    @property
    def src_end(self):
        """Get the end point of the row."""
        return self.src_start + self.range_length

    @property
    def offset(self):
        """Get the amount to move from src to destination."""
        return self.dest_start - self.src_start

    def __repr__(self) -> str:
        """Show a string representation of this record."""
        return f"[{self.src_start},{self.src_end})=>{self.offset:+}"


def read_input(input: str):
    """Convert the input to seeds, paths and the almanac."""
    _seeds, _, maps = input.split("\n", maxsplit=2)

    paths = ["seed"]
    almanac: Mapping[tuple[str, str], list[AlmanacRow]] = defaultdict(list)

    for m in MAPS.finditer(maps):
        src_name, dest_name, _ranges = m.groups()
        paths.append(dest_name)
        for ranges in _ranges.splitlines():
            almanac[(src_name, dest_name)].append(
                AlmanacRow(*map(int, DIGIT.findall(ranges)))
            )
    seeds = tuple(map(int, DIGIT.findall(_seeds)))
    return seeds, paths, dict(almanac)


def converter_factory(row: AlmanacRow) -> Callable[[int], int | None]:
    """Create a converter that uses the range information."""
    dest_start, src_start, range_length = row
    max_src = src_start + range_length
    diff = dest_start - src_start

    def converter(x: int) -> int | None:
        if src_start <= x < max_src:
            return diff + x
        return None

    return converter


def trails(input: str) -> tuple[Paths, ItemizedSeedMappings]:
    """Find the paths and the seed mappings from the input text.

    Use the `read_input` function to return the seeds, paths and the encodings
    for the almanac. Create a converter that takes each seed and converts it
    to the next level and keep a record of it.

    Parameters
    ----------
    input : str
        The string describing the seeds and how to convert from seeds to
        locations.

    Returns
    -------
    tuple[Paths, SeedMappings]
        A tuple containing the relationships (e.g. `seed`, `soil`,...) and then
        the mappings for each starting seed (seed) : (seed, soil). Such that a
        dictionary can be made from each path and seed to find the exact trail
        that has been traced.
    """
    seeds, paths, _almanac = read_input(input)
    almanac: Mapping[tuple[str, str], list[Callable[[int], int | None]]] = {
        k: [converter_factory(w) for w in v] for k, v in _almanac.items()
    }
    mapped: ItemizedSeedMappings = {}
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
    """Find the lowest location at a specific position

    The calculation assume the seeds are individual starting points."""
    paths, mappings = trails(input)
    i = paths.index(loc)
    return min(mapping[i] for mapping in mappings.values())


def ranged_converter_factory(
    almanac: Sequence[AlmanacRow],
) -> Callable[[tuple[int, int]], Sequence[tuple[int, int]]]:
    """Create a converter using the almanac over ranges.

    The converter works by sorting the almanac rows and, if the item is
    out-of-range, will return the item as is. If in range, it will find the
    specific range that is relevant for the start and stop of the range. If
    these are the same almanac record, then use a single converter.
    If it spans multiple ranges, split the first and last range on its overlap;
    and then convert the intermediate ranges as the span the full range of
    values.

    Parameters
    ----------
    almanac : Sequence[AlmanacRow]
        A sequence of the raw almanac records.

    Returns
    -------
    Callable[[tuple[int, int]], Sequence[tuple[int, int]]]
        The converter as described in the description.
    """
    _almanac = sorted(almanac, key=lambda row: row.src_start)

    almanac = [_almanac[0]]
    for a in _almanac[1:]:
        if span := (a.src_start - almanac[-1].src_end):
            almanac.append(
                AlmanacRow(
                    almanac[-1].src_end,
                    almanac[-1].src_end,
                    span,
                )
            )

        almanac.append(a)
    almanac_start, almanac_end = _almanac[0].src_start, _almanac[-1].src_end

    def convert(val: tuple[int, int]) -> Sequence[tuple[int, int]]:
        start, stop = val[0], val[0] + val[1]
        if start >= almanac_end or stop <= almanac_start:
            return (val,)
        start_grp, stop_grp = (
            bisect.bisect_right(almanac, start, key=lambda row: row.src_start),
            bisect.bisect_left(almanac, stop, key=lambda row: row.src_start),
        )
        if start_grp == 0:
            return (val,)
        if start_grp == stop_grp:
            return ((val[0] + almanac[start_grp - 1].offset, val[1]),)
        first, *intermediate, last = almanac[start_grp - 1 : stop_grp]
        result = [
            (start + first.offset, first.src_end - start),
            *[(row.dest_start, row.range_length) for row in intermediate],
            (last.src_start + last.offset, stop - last.src_start),
        ]
        return tuple(result)

    return convert


def ranged_trails(input: str) -> dict[str, Sequence[tuple[int, int]]]:
    """Find the ranges that map to each layer."""
    _seeds, paths, _almanac = read_input(input)
    results: dict[str, Sequence[tuple[int, int]]] = dict(
        seed=tuple((a, b) for a, b in zip(_seeds[0::2], _seeds[1::2]))
    )

    for src_name, dest_name in zip(paths[:-1], paths[1:]):
        almanac = ranged_converter_factory(_almanac[(src_name, dest_name)])
        output = ()
        for src in results[src_name]:
            output = (*output, *almanac(src))

        results[dest_name] = output
    return results


def lowest_ranged_location(input: str, loc: str) -> int:
    """Find the lower location at a specific position."""

    paths = ranged_trails(input)
    return min(el[0] for el in paths[loc])


def main():
    """Find the results for part one and two."""
    with utils.contents() as contents:
        utils.print_part_one( lowest_location(contents, "location"))
        utils.print_part_two( lowest_ranged_location(contents, "location"))


if __name__ == "__main__":
    main()
