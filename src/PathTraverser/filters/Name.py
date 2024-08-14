import fnmatch
import re
from .Generic import Filter, MutableFilter
from pathlib import Path
from typing import  Callable


class name(MutableFilter):

    _names: set[str]
    _patterns: tuple[ re.Pattern]

    def __init__(self, *names: str | re.Pattern) -> None:
        super().__init__()
        self._names = set(_ for _ in names if isinstance(_, str))
        self._patterns = tuple(_ for _ in names if isinstance(_, re.Pattern))

    def __call__(self, *names: str | re.Pattern) -> Filter:
        return self.__class__(*names)

    def __eq__(self, other: str | re.Pattern | list[str | re.Pattern]) -> Filter:
        if isinstance(other, str) or isinstance(other, re.Pattern):
            return self.__class__(other)
        elif isinstance(other, list):
            if any(_ for _ in other if not (isinstance(_, str) or isinstance(_, re.Pattern))):
                return NotImplemented
            return self.__class__(*other)
        return NotImplemented

    def regex(self, *patterns: str) -> Filter:
        return self.__class__(*(
            (re.compile(_) if isinstance(_, str) else _) for _ in patterns
            if (isinstance(_, str) or isinstance(_, re.Pattern))
        ))

    def glob(self, *patterns: str) -> Filter:
        return self.regex(*(fnmatch.translate(_) for _ in patterns if isinstance(_, str)))

    def filter(
            self,
            root: Path,
            absolute_path: Path,
            relative_path: Path,
            depth: int,
            skipsubtree: Callable) -> bool:
        name: str = relative_path.name
        match: bool = False
        if self._names and name in self._names:
            match = True
        elif self._patterns:
            for pattern in self._patterns:
                if match := bool(re.match(pattern, name)):
                    break
        return match if self.is_positive else not match


name = name()
