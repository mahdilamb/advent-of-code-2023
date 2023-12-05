import re

from advent_of_code import utils


CARD_WINNING_MINE = re.compile(r"Card\s*(\d+):\s*(.*?)\s*\|\s*(.*)")
DIGITS = re.compile(r"\d+")


def scores(input: str) -> dict[int, int]:
    """Calculate the core for each scratch card."""
    results = {}
    for match in CARD_WINNING_MINE.finditer(input):
        card, _winning, _mine = match.groups()
        winning = set(DIGITS.findall(_winning))
        mine = set(DIGITS.findall(_mine))
        matches = mine & winning
        if len(matches):
            results[int(card)] = 2 ** (len(matches) - 1)
        else:
            results[int(card)] = 0
    return results


def main():
    with utils.contents() as contents:
        print(scores(contents))
        print("Part one:", sum(scores(contents).values()))


if __name__ == "__main__":
    main()
