from pathlib import Path
from typing import Callable
from itertools import chain


class Filter:

    def __add__(self, other: 'Filter') -> 'Filter':
        if isinstance(other, Filter):
            return OrFilter(self, other)
        else:
            return NotImplemented

    @property
    def is_positive(self) -> bool:
        raise NotImplementedError("Method not implemented!")

    def __neg__(self) -> 'Filter':
        raise NotImplementedError("Method not implemented!")

    def __pos__(self) -> 'Filter':
        raise NotImplementedError("Method not implemented!")

    def filter(self, root: Path, absolute_path: Path, relative_path: Path, depth: int, skipsubtree: Callable) -> bool:
        raise NotImplementedError("Method not implemented!")


class MutableFilter(Filter):

    _is_positive: bool = True

    @property
    def is_positive(self) -> bool:
        return self._is_positive

    def __neg__(self) -> Filter:
        self._is_positive = False
        return self

    def __pos__(self) -> Filter:
        self._is_positive = True
        return self


class OrFilter(MutableFilter):

    _filters: tuple[Filter]

    def __init__(self, *filters: Filter) -> None:
        super().__init__()
        self._filters = tuple(chain.from_iterable(_._filters if isinstance(_, OrFilter) else [_] for _ in filters))

    def filter(self, root: Path, absolute_path: Path, relative_path: Path, depth: int, skipsubtree: Callable) -> bool:
        # INFO: turn off "skipsubtree" for filters run in "or" chain
        is_any: bool = \
            any(filter.filter(root, absolute_path, relative_path, depth, lambda _: ...) for filter in self._filters)
        return is_any if self.is_positive else not is_any
