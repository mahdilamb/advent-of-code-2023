"""Tests for day 5."""
from typing import Callable, Generator, Sequence
from advent_of_code import day_05
import pytest


@pytest.fixture
def sample() -> str:
    """Fixture with Day 5 sample."""
    return r"""seeds: 79 14 55 13

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
56 93 4"""


@pytest.fixture
def sample_converter() -> Generator[Callable, None, None]:
    """Fixture with a sample converter."""
    converter = day_05.ranged_converter_factory(
        [day_05.AlmanacRow(20, 0, 10), day_05.AlmanacRow(17, 12, 2)]
    )
    yield converter


def test_part_one(sample):
    """Test that part one works according the sample given."""
    assert (
        day_05.lowest_location(
            sample,
            "location",
        )
        == 35
    )


@pytest.mark.parametrize(
    ("location", "test", "result"),
    [
        ("before start", (-2, 1), ((-2, 1),)),
        ("start on", (-1, 1), ((-1, 1),)),
        ("start-edge", (0, 1), ((20, 1),)),
        ("in", (2, 1), ((22, 1),)),
        ("gap", (11, 1), ((11, 1),)),
        ("end-on", (13, 1), ((18, 1),)),
        ("other", (13, 1), ((18, 1),)),
        ("end-edge", (14, 1), ((14, 1),)),
        ("after", (100, 1), ((100, 1),)),
        ("over", (8, 3), ((28, 2), (10, 1))),
        ("over multiple", (8, 5), ((28, 2), (10, 2), (17, 1))),
    ],
    ids=lambda val: (val,) if isinstance(val, str) else "",
)
def test_range_converter(
    sample_converter,
    location: str,
    test: tuple[int, int],
    result: Sequence[tuple[int, int]],
):
    """Test the range converter."""
    assert (
        sample_converter(test) == result
    ), f"Expected the sample [{str(test)[1:-1]}) in '{location}' to return {result}."


def test_part_two(sample):
    """Test that part two works correctly based on the example given."""
    assert day_05.lowest_ranged_location(sample, "location") == 46


if __name__ == "__main__":
    import sys

    sys.exit(pytest.main([__file__] + ["-vv", "-s"]))
