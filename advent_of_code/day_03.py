import re
import numpy as np
from scipy.ndimage import maximum_filter, label
import advent_of_code.utils as utils

SYMBOL = re.compile(r"([^.\d]+)", re.M)
NUMBER = re.compile(r"([\d]+)", re.M)
GEAR = re.compile(r"\*", re.M)


def gear_mask(text: np.ndarray) -> np.ndarray:
    """Get a boolean mask containing the location of gears."""
    return np.vectorize(GEAR.match, otypes=(bool,))(text)


def number_mask(text: np.ndarray) -> np.ndarray:
    """Get a boolean mask containing the position of numbers."""
    return np.vectorize(NUMBER.match, otypes=(bool,))(text)


def symbol_mask(text: np.ndarray) -> np.ndarray:
    """Get a boolean mask containing the position of symbols."""
    return np.vectorize(SYMBOL.match, otypes=(bool,))(text)


def get_gear_ratios(text: str) -> tuple[int, ...]:
    """Get the gear ratios from a string."""
    lines = text.splitlines()
    arr = np.asarray(tuple(tuple(line) for line in lines))
    gears = gear_mask(arr)
    numbers = number_mask(arr)
    labeled_numbers, _ = label(numbers, structure=(((0, 0, 0), (1, 1, 1), (0, 0, 0))))
    number_or_gear_expanded, _ = label((numbers | gears), structure=np.ones((3, 3)))
    results: list[int] = []

    for gear_x, gear_y in zip(*np.where(gears)):
        gear_neighbours = (
            number_or_gear_expanded == number_or_gear_expanded[gear_x][gear_y]
        )
        gear_numbers = labeled_numbers * gear_neighbours
        ids = np.unique(gear_numbers)[1:]
        if len(ids) != 2:
            continue
        results.append(
            int("".join(arr[labeled_numbers == ids[0]]))
            * int("".join(arr[labeled_numbers == ids[1]]))
        )

    return tuple(results)


def get_part_numbers(text: str) -> tuple[int, ...]:
    """Get the part numbers from text."""
    lines = text.splitlines()
    arr = np.asarray(tuple(tuple(line) for line in lines))
    masked = symbol_mask(arr)
    masked_neighbor = maximum_filter(masked, size=(3, 3), mode="constant")
    numbers = number_mask(arr)
    labeled, _ = label(numbers, structure=(((0, 0, 0), (1, 1, 1), (0, 0, 0))))
    results: list[int] = []
    for i in range(masked_neighbor.shape[0]):
        ids = np.unique(masked_neighbor[i, :] * labeled[i, :])[1:]
        for id in ids:
            results.append(
                int("".join((np.asarray(tuple(lines[i]))[labeled[i, :] == id])))
            )

    return tuple(results)


def main():
    with utils.contents() as contents:
        print("Part one:", sum(get_part_numbers((contents))))
        print("Part two:", sum(get_gear_ratios((contents))))


if __name__ == "__main__":
    main()
