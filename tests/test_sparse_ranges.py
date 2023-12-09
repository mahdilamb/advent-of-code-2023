from advent_of_code import sparse_ranges


def test_overlap():
    a = sparse_ranges.SparseRange(1, 4)
    assert sparse_ranges.overlaps(
        a, sparse_ranges.SparseRange(1, 4)
    ), "Expected same range to overlap"
    assert not sparse_ranges.overlaps(
        a, sparse_ranges.SparseRange(-1, 1)
    ), "Expected prior not to overlap."
    assert sparse_ranges.overlaps(
        a, sparse_ranges.SparseRange(0, 1)
    ), "Expected prior tip to overlap."
    assert not sparse_ranges.overlaps(
        a, sparse_ranges.SparseRange(6, 1)
    ), "Expected post not to overlap."
    assert sparse_ranges.overlaps(
        a, sparse_ranges.SparseRange(5, 1)
    ), "Expected post tip to overlap."
    assert sparse_ranges.overlaps(
        a, sparse_ranges.SparseRange(2, 4)
    ), "Expected greater range to overlap."
    assert sparse_ranges.overlaps(
        a, sparse_ranges.SparseRange(0, 4)
    ), "Expected greater range to overlap."


def test_split():
    a = sparse_ranges.SparseRange(5, 10)
    assert (
        sum(
            el is not None
            for el in sparse_ranges.split(a, sparse_ranges.SparseRange(0, 2))
        )
        == 0
    ), "Expected non-overlapping to return no splits"
    assert (
        sum(
            el is not None
            for el in sparse_ranges.split(a, sparse_ranges.SparseRange(9, 17))
        )
        == 2
    ), "Expected overlap on right to return 2 splits."
    assert (
        sum(
            el is not None
            for el in sparse_ranges.split(a, sparse_ranges.SparseRange(4, 2))
        )
        == 2
    ), "Expected overlap on left to return 2 splits."
    assert (
        sum(
            el is not None
            for el in sparse_ranges.split(a, sparse_ranges.SparseRange(6, 2))
        )
        == 3
    ), "Expected overlap in center to return three splits."


def test_merge():
    assert (
        len(
            sparse_ranges.merge(
                sparse_ranges.SparseRange(1, 4),
                sparse_ranges.SparseRange(2, 4),
                sparse_ranges.SparseRange(0, 4),
            )
        )
        == 1
    ), "Expected all to merged"
    assert (
        len(
            sparse_ranges.merge(
                sparse_ranges.SparseRange(6, 4),
                sparse_ranges.SparseRange(1, 4),
                sparse_ranges.SparseRange(7, 2),
            )
        )
        == 2
    ), "Expected some to merge."


def test_translation():
    def convert(input: str) -> tuple[tuple[int, int, int], ...]:
        return tuple(tuple(map(int, line.split())) for line in input.splitlines())

    seed_to_soil = {
        sparse_ranges.SparseRange(src, length): dest - src
        for dest, src, length in convert(
            """50 98 2
52 50 48"""
        )
    }

    soil_to_fertilizer = {
        sparse_ranges.SparseRange(src, length): dest - src
        for dest, src, length in convert(
            """0 15 37
37 52 2
39 0 15"""
        )
    }
    fertilizer_to_water = {
        sparse_ranges.SparseRange(src, length): dest - src
        for dest, src, length in convert(
            """49 53 8
0 11 42
42 0 7
57 7 4"""
        )
    }
    water_to_light = {
        sparse_ranges.SparseRange(src, length): dest - src
        for dest, src, length in convert(
            """88 18 7
18 25 70"""
        )
    }
    light_to_temperature = {
        sparse_ranges.SparseRange(src, length): dest - src
        for dest, src, length in convert(
            """45 77 23
81 45 19
68 64 13"""
        )
    }
    temperature_to_humidity = {
        sparse_ranges.SparseRange(src, length): dest - src
        for dest, src, length in convert(
            """0 69 1
1 0 69"""
        )
    }
    humidity_to_location = {
        sparse_ranges.SparseRange(src, length): dest - src
        for dest, src, length in convert(
            """60 56 37
56 93 4"""
        )
    }
    seeds = [sparse_ranges.SparseRange(79, 14), sparse_ranges.SparseRange(55, 13)]
    soils = [
        soil for seed in seeds for soil in sparse_ranges.translate(seed, seed_to_soil)
    ]
    assert soils == [(81, 14), (57, 13)]
    fertilizers = [
        fertilizer
        for soil in soils
        for fertilizer in sparse_ranges.translate(soil, soil_to_fertilizer)
    ]
    assert fertilizers == [(81, 14), (57, 13)]
    waters = [
        water
        for fertilizer in fertilizers
        for water in sparse_ranges.translate(fertilizer, fertilizer_to_water)
    ]
    print(waters, [(81, 14), (57, 13)])
    lights = [
        light
        for water in waters
        for light in sparse_ranges.translate(water, water_to_light)
    ]
    temperatures = [
        temperature
        for light in lights
        for temperature in sparse_ranges.translate(light, light_to_temperature)
    ]
    humidities = [
        humidity
        for temperature in temperatures
        for humidity in sparse_ranges.translate(temperature, temperature_to_humidity)
    ]
    locations = [
        location
        for humidity in humidities
        for location in sparse_ranges.translate(humidity, humidity_to_location)
    ]
    print(locations)


if __name__ == "__main__":
    import pytest
    import sys

    sys.exit(pytest.main([__file__] + ["-vv", "-s"]))
