import glob
import re
from .Generic import Filter, MutableFilter
from pathlib import Path
from typing import  Callable


class path(MutableFilter):

    _paths: set[str]
    _patterns: tuple[ re.Pattern]

    def __init__(self, *paths: str | re.Pattern) -> None:
        super().__init__()
        self._paths = set(_ for _ in paths if isinstance(_, str))
        self._patterns = tuple(_ for _ in paths if isinstance(_, re.Pattern))

    def __call__(self, *paths: str | re.Pattern) -> Filter:
        return self.__class__(*paths)

    def __eq__(self, other: str | re.Pattern | list[str | re.Pattern]) -> Filter:
        if isinstance(other, str) or isinstance(other, re.Pattern):
            return self.__class__(other)
        elif isinstance(other, list):
            if any(_ for _ in other if not (isinstance(_, str) or isinstance(_, re.Pattern))):
                return NotImplemented
            return self.__class__(*other)
        return NotImplemented

    def regex(self, *patterns: str) -> Filter:
        return self.__class__(*(re.compile(_) for _ in patterns if isinstance(_, str)))

    def glob(self, *patterns: str) -> Filter:
        # WARN: from python 3.13
        return self.regex(
            *(glob.translate(_, recursive=True, include_hidden=True) for _ in patterns if isinstance(_, str)))

    def filter(
            self,
            root: Path,
            absolute_path: Path,
            relative_path: Path,
            depth: int,
            skipsubtree: Callable) -> bool:
        path: str = str(absolute_path)
        match: bool = False
        if self._paths and path in self._paths:
            match = True
        elif self._patterns:
            for pattern in self._patterns:
                if match := bool(re.match(pattern, path)):
                    break
        return match if self.is_positive else not match


path = path()
