import re
from typing import Callable

from advent_of_code import utils


CARD_WINNING_MINE = re.compile(r"Card\s*(\d+):\s*(.*?)\s*\|\s*(.*)")
DIGITS = re.compile(r"\d+")


def scores(
    input: str, calc_score: Callable[[int], int] = lambda x: 2 ** (x - 1)
) -> dict[int, int]:
    """Calculate the core for each scratch card."""
    results = {}
    for match in CARD_WINNING_MINE.finditer(input):
        card, _winning, _mine = match.groups()
        winning = set(DIGITS.findall(_winning))
        mine = set(DIGITS.findall(_mine))
        matches = mine & winning
        if len(matches):
            results[int(card)] = calc_score(len(matches))
        else:
            results[int(card)] = 0
    return results


def num_cards(input: str) -> int:
    """Count the number of cards."""
    card_scores = scores(input, calc_score=lambda x: x)
    cards = sorted(card_scores)
    winnings = []

    def count_cards(card: int) -> None:
        score = card_scores[card]
        last_card = min(card + score, cards[-1])
        winnings.extend(cards[card:last_card])
        for c in cards[card:last_card]:
            count_cards(c)

    for card in cards:
        count_cards(card)
    return len(winnings) + len(cards)


def main():
    with utils.contents() as contents:
        print("Part one:", sum(scores(contents).values()))
        print("Part two:", num_cards(contents))


if __name__ == "__main__":
    main()
