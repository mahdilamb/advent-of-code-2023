import math
import re
from typing import Callable, Literal, TypeAlias
import typing
import advent_of_code.utils as utils

ColorNames: TypeAlias = Literal["red", "green", "blue"]

ID_TO_CALLS = re.compile(r"Game (\d+)?: (.*)", re.M)
COLORS: dict[ColorNames, re.Pattern] = {
    color: re.compile(rf"(\d+)\s{color}") for color in typing.get_args(ColorNames)
}


def max_per_game(games: str) -> dict[int, dict[ColorNames, int]]:
    """Calculate the maximum number of balls per color per game."""
    games_with_ids = ID_TO_CALLS.findall(games)
    result = {}
    for id, calls in games_with_ids:
        result[int(id)] = {
            color: max(map(int, pattern.findall(calls)))
            for color, pattern in COLORS.items()
        }
    return result


def possible_games(
    max_balls: dict[ColorNames, int],
) -> Callable[[str], tuple[int, ...]]:
    """Get a function used to filter the games and return possible IDs given a dictionary containing the maximum number of balls of each color."""

    def filter_games(games: str):
        return tuple(
            id
            for id, maxes in max_per_game(games).items()
            if all(
                maxes[color] <= max_balls[color]
                for color in typing.get_args(ColorNames)
            )
        )

    return filter_games


def sum_of_powers(games: str):
    """Calculate the sum of the powers of each game."""
    return sum(math.prod(game.values()) for game in max_per_game(games).values())


def main():
    with utils.contents() as contents:
        print(
            "Part one:",
            sum(possible_games({"red": 12, "green": 13, "blue": 14})(contents)),
        )
        print("Part two:", sum_of_powers(contents))


if __name__ == "__main__":
    main()
