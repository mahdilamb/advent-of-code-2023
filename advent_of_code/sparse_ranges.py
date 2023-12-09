from typing import Iterator, Mapping, NamedTuple, Sequence, Union


class SparseRange(NamedTuple):
    start: int
    length: int

    @property
    def end(self) -> int:
        """Get the end of the range."""
        return self.start + self.length

    def __contains__(self, x: Union["SparseRange", int]) -> bool:
        """Check if a int or range is contained within this one."""
        if isinstance(x, int):
            return self.start <= x < self.end
        return x.start >= self.start and x.end < self.end

    def __iter__(self) -> Iterator[int]:
        """Iterate over the length."""
        yield from range(self.start, self.start + self.length)

    def __len__(self) -> int:
        """Get the length of the range."""
        return self.length

    def __repr__(self) -> str:
        return f"{self.start} -> {self.end}"

    def __sub__(self, x: int):
        return SparseRange(self.start - x, self.length)

    def __add__(self, x: int):
        return SparseRange(self.start + x, self.length)


def overlaps(a: SparseRange, b: SparseRange) -> bool:
    """Check if another range overlaps with this one."""
    return (a.start <= b.end) and (b.start <= a.end)


def split(
    src: SparseRange, by: SparseRange
) -> (
    tuple[None, None, None] | tuple[SparseRange | None, SparseRange, SparseRange | None]
):
    """Split the range and get a tuple of the ranges [before, overlapping, after] the split.

    The output range will span the src range."""
    if not overlaps(src, by):
        return (None, None, None)
    max_start = max(by.start, src.start)
    min_end = min(by.end, src.end)
    output = (
        None,
        SparseRange(max_start, min_end - max_start),
        None,
    )
    if by.start > src.start:
        output = SparseRange(src.start, by.start - src.start), *output[1:]
    if src.end > by.end:
        output = *output[:2], SparseRange(by.end, src.end - by.end)
    return output


def merge(*ranges: SparseRange) -> tuple[SparseRange, ...]:
    result = sorted(ranges, key=lambda x: (x.start, -x.length))
    for i in reversed(range(len(result))):
        if not i:
            break
        if overlaps(result[i], (merge_with := result[i - 1])):
            to_merge = result.pop(i)
            result[i - 1] = SparseRange(
                merge_with.start,
                max(to_merge.end, merge_with.end) - merge_with.start,
            )
    return tuple(result)


def translate(
    src: SparseRange, map: Mapping[SparseRange, int]
) -> Sequence[SparseRange]:
    pool = [src]
    for split_by, translation in map.items():
        new_pool = []
        for frag in pool:
            before, overlap, after = split(frag, split_by)
            if overlap is None:
                continue
            if before is not None:
                new_pool.append(before)
            new_pool.append(overlap + translation)
            if after is not None:
                new_pool.append(after)
        pool = new_pool or pool
    return merge(*pool)
