from advent_of_code import day_06
import pytest


@pytest.fixture
def sample():
    return """Time:      7  15   30
Distance:  9  40  200"""


@pytest.mark.parametrize(
    ("time_button_down", "distance_moved"),
    [
        (0, 0),
        (1, 6),
        (2, 10),
        (3, 12),
        (4, 12),
        (5, 10),
        (6, 6),
        (7, 0),
    ],
)
def test_first_race(time_button_down: int, distance_moved: int):
    assert day_06.race(duration=7, held_for=time_button_down) == distance_moved


def test_first_race_combos():
    assert day_06.first_race_combos() == (2, 3, 4, 5)


def test_second_race_combos():
    assert day_06.race_combos(race_duration=15, record_distance=40) == tuple(
        range(4, 12)
    )


def test_third_race_combos():
    assert day_06.third_race_combos() == tuple(range(11, 20))


def test_margin_of_error():
    assert (
        day_06.margin_of_error(
            day_06.first_race_combos(),
            day_06.second_race_combos(),
            day_06.third_race_combos(),
        )
        == 288
    )


def test_margin_of_error_from_input(sample):
    assert day_06.margin_of_error(*day_06.parse_input_to_race_combos(sample)) == 288


def test_margin_of_error_from_input_with_kerning_fixed(sample):
    assert day_06.margin_of_error_optimized(sample) == 71503


if __name__ == "__main__":
    import sys

    sys.exit(pytest.main([__file__] + ["-vv", "-s"]))
