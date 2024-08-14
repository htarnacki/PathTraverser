from .Generic import Filter, MutableFilter
from pathlib import Path
from typing import Callable


class depth(MutableFilter):

    _min_depth: int
    _max_depth: int

    def __init__(self, min_depth: int = None, max_depth: int = None) -> None:
        super().__init__()
        self._min_depth = min_depth
        self._max_depth = max_depth

    def __eq__(self, depth: int) -> Filter:
        if not isinstance(depth, int):
            return NotImplemented
        self._min_depth = depth
        self._max_depth = depth
        return self
    
    def __ne__(self, depth: int) -> Filter:
        if not isinstance(depth, int):
            return NotImplemented
        return -(self == depth)

    def __lt__(self, depth: int) -> Filter:
        if not isinstance(depth, int):
            return NotImplemented
        self._max_depth=depth - 1
        return self

    def __le__(self, depth: int) -> Filter:
        if not isinstance(depth, int):
            return NotImplemented
        self._max_depth=depth
        return self

    def __ge__(self, depth: int) -> Filter:
        if not isinstance(depth, int):
            return NotImplemented
        self._min_depth=depth
        return self

    def __gt__(self, depth: int) -> Filter:
        if not isinstance(depth, int):
            return NotImplemented
        self._min_depth=depth + 1
        return self

    def filter(
            self,
            root: Path,
            absolute_path: Path,
            relative_path: Path,
            depth: int,
            skipsubtree: Callable) -> bool:
        if self.is_positive:
            if depth == self._max_depth and absolute_path.is_dir():
                skipsubtree(absolute_path)
        else:
            if self._max_depth is None and depth == self._min_depth and absolute_path.is_dir():
                skipsubtree(absolute_path)
        min_depth: int = self._min_depth if self._min_depth is not None else depth
        max_depth: int = self._max_depth if self._max_depth is not None else depth
        in_range: bool = min_depth <= depth <= max_depth
        return in_range if self.is_positive else not in_range
