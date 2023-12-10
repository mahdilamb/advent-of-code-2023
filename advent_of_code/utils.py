import contextlib
import glob
import inspect
import os
import re
from typing import Literal

import advent_of_code


@contextlib.contextmanager
def contents():  # pragma: no cover
    frame_records = inspect.stack()[2]
    calling_module = inspect.getmodulename(frame_records[1])
    with open(
        os.path.normpath(
            os.path.join(__file__, "..", "inputs", f"{calling_module}.txt")
        ),
        "r",
    ) as fp:
        yield fp.read()


def print_part_one(*args, **kwargs):  # pragma: no cover
    """Print part one."""
    print("Part 1", *args, **kwargs)


def print_part_two(*args, **kwargs):  # pragma: no cover
    """Print part two."""
    print("Part 2", *args, **kwargs)


def version():  # pragma: no cover
    PART = re.compile(r"(print_part_one)\([\s\S]*?(print_part_two|\Z)")

    def part(file: str) -> tuple[int, Literal[1, 2]] | None:
        with open(file) as fp:
            try:
                return int(os.path.basename(file)[4:6]), len(
                    tuple(
                        filter(
                            lambda match: match,
                            next(PART.finditer(fp.read())).groups(),
                        )
                    )
                )
            except StopIteration:
                return None
            finally:
                ...

    days = sorted(
        glob.glob(os.path.join(os.path.dirname(advent_of_code.__file__), "day_*.py"))
    )[::-1]
    day_done, part_done = next(
        filter(lambda el: el is not None, (part(day) for day in days))
    )
    return f"2023.12.{day_done:02d}_{part_done}"
