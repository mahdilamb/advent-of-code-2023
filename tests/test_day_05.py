from advent_of_code import day_05

TEST = r"""seeds: 79 14 55 13

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


def test_part_one():
    assert (
        day_05.lowest_location(
            TEST,
            "location",
        )
        == 35
    )


def test_part_two():
    assert day_05.lowest_location(TEST, "location", seeds_as_ranges=True) == 46


if __name__ == "__main__":
    import pytest
    import sys

    sys.exit(pytest.main([__file__] + ["-vv", "-s"]))
