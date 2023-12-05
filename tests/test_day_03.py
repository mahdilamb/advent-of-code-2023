from advent_of_code import day_03


def test_part_one():
    """Test part numbers."""
    assert (
        sum(
            day_03.get_part_numbers(
                """467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598.."""
            )
        )
        == 4361
    )


def test_part_two():
    """Test gear ratios."""
    assert (
        sum(
            day_03.get_gear_ratios(
                """467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..""",
            )
        )
        == 467835
    )


if __name__ == "__main__":
    import pytest
    import sys

    sys.exit(pytest.main([__file__] + ["-vv", "-s"]))
