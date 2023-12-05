import re

import utils

FIRST_AND_LAST_DIGIT = re.compile(r"(?:(\d).*(\d+)(?!.*\d)|(\d))")
NUMBER_NAMES: dict[str, str] = {
    j: str(i)
    for i, j in enumerate(
        ("one", "two", "three", "four", "five", "six", "seven", "eight", "nine"),
        start=1,
    )
}
FIRST_AND_LAST_DIGIT_EXTENDED = re.compile(
    r"(?:({d}).*({d}+)(?!.*{d})|({d}))".format(d=rf"\d|{'|'.join(NUMBER_NAMES.keys())}")
)


def maybe_spelt(val: str) -> str:
    """Convert a value (either a single digit or that digit spelt out) into just a single digit."""
    return NUMBER_NAMES.get(val, val)


def identity(val: str) -> str:
    """Return the value as is."""
    return val


def document_calibration(document: str, use_extended: bool = True) -> int:
    """Calculate the calibration value of a document."""
    if use_extended:
        pattern = FIRST_AND_LAST_DIGIT_EXTENDED
        num = maybe_spelt
    else:
        pattern = FIRST_AND_LAST_DIGIT
        num = identity

    def line_calibration(line: str) -> int:
        """Calculate the calibration value of a line."""
        first, last, any = next(pattern.finditer(line)).groups()
        if any is not None:
            return int(num(any) + num(any))
        return int(num(first) + num(last))

    return sum(map(line_calibration, document.splitlines()))


def main():
    with utils.contents() as contents:
        print("Part one:", document_calibration(contents, use_extended=False))
        print("Part two:", document_calibration(contents))


if __name__ == "__main__":
    main()
