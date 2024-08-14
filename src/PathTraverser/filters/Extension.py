from .Generic import  Filter, MutableFilter
from pathlib import Path
from typing import  Callable


class ext(MutableFilter):

    _ext: set[str]

    def __init__(self, *ext: str) -> None:
        super().__init__()
        self._ext = set(ext)

    def __call__(self, *ext: str) -> Filter:
        return self.__class__(*ext)

    def __getattr__(self, name: str) -> Filter:
        return self.__class__(*self._ext, name)

    def __add__(self, other: Filter) -> Filter:
        if isinstance(other, self.__class__):
            return self.__class__(*self._ext, *other._ext)
        elif isinstance(other, Filter):
            return super().__add__(other)
        else:
            return NotImplemented

    def filter(
            self,
            root: Path,
            absolute_path: Path,
            relative_path: Path,
            depth: int,
            skipsubtree: Callable) -> bool:
        in_set: bool = relative_path.suffix[1:] in self._ext
        return in_set if self.is_positive else not in_set


ext = ext()
