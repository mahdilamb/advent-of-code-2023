import re
import numpy as np
from scipy.ndimage import maximum_filter, label
import utils

SYMBOL = re.compile(r"([^.\d]+)", re.M)
NUMBER = re.compile(r"([\d]+)", re.M)


def number_mask(text: np.ndarray) -> np.ndarray:
    return np.vectorize(NUMBER.match, otypes=(bool,))(text)


def symbol_mask(text: np.ndarray) -> np.ndarray:
    return np.vectorize(SYMBOL.match, otypes=(bool,))(text)


def get_part_numbers(text: str) -> tuple[int, ...]:
    lines = text.splitlines()
    arr = np.asarray(tuple(tuple(line) for line in lines))
    symbol = symbol_mask(arr)
    symbol_neighbor = maximum_filter(symbol, size=(3, 3), mode="constant")
    numbers = number_mask(arr)
    labeled, _ = label(numbers, structure=(((0, 0, 0), (1, 1, 1), (0, 0, 0))))
    results: list[int] = []
    for i in range(len(lines)):
        ids = set(symbol_neighbor[i, :] * labeled[i, :]) - {0}
        if ids:
            for id in ids:
                results.append(
                    int("".join((np.asarray(tuple(lines[i]))[labeled[i, :] == id])))
                )

    return tuple(results)


def main():
    with utils.contents() as contents:
        print("Part one:", sum(get_part_numbers((contents))))


if __name__ == "__main__":
    main()
