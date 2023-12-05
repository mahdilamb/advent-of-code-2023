from advent_of_code import day_01


def test_part_one():
    """Test calibration value using digits only."""
    assert (
        day_01.document_calibration(
            """1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet""",
            use_extended=False,
        )
        == 142
    )


def test_part_two():
    """Test calibration that allows single digits to be spelt out."""
    assert (
        day_01.document_calibration(
            """two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen"""
        )
        == 281
    )


if __name__ == "__main__":
    import pytest
    import sys

    sys.exit(pytest.main([__file__] + ["-vv", "-s"]))
