import os
from .Generic import Filter, MutableFilter
from pathlib import Path
from typing import  Callable
from ..utils.Os import is_hidden, is_readonly, is_executable, is_writeable, \
    get_owner


class hidden(MutableFilter):

    def filter(
            self,
            root: Path,
            absolute_path: Path,
            relative_path: Path,
            depth: int,
            skipsubtree: Callable) -> bool:
        return is_hidden(absolute_path) if self.is_positive else not is_hidden(absolute_path)


class readonly(MutableFilter):

    def filter(
            self,
            root: Path,
            absolute_path: Path,
            relative_path: Path,
            depth: int,
            skipsubtree: Callable) -> bool:
        return is_readonly(absolute_path) if self.is_positive else not is_readonly(absolute_path)


class executable(MutableFilter):

    def filter(
            self,
            root: Path,
            absolute_path: Path,
            relative_path: Path,
            depth: int,
            skipsubtree: Callable) -> bool:
        return is_executable(absolute_path) if self.is_positive else not is_executable(absolute_path)


class writeable(MutableFilter):

    def filter(
            self,
            root: Path,
            absolute_path: Path,
            relative_path: Path,
            depth: int,
            skipsubtree: Callable) -> bool:
        return is_writeable(absolute_path) if self.is_positive else not is_writeable(absolute_path)


class size(MutableFilter):

    _min_size: int
    _max_size: int

    @staticmethod
    def _human_read_to_byte(size: str) -> int:
        factors: dict[str, int] = {
            'B' : 1,
            'KB': 1024,
            'MB': 1048576,
            'GB': 1073741824,
            'TB': 1099511627776,
            'PB': 1125899906842624,
            'EB': 1152921504606846976 ,
            'ZB': 1180591620717411303424,
            'YB': 1208925819614629174706176
        }
        size = size.strip()
        if (unit := size[-2:]) in factors.keys():
            return factors[unit] * int(size[:-2].strip())
        elif (unit := size[-1:]) == 'B':
            return factors[unit] * int(size[:-1].strip())
        else:
            raise ValueError('Unknown file size unit!')

    def __init__(self, min_size: int | str = None, max_size: int | str = None) -> None:
        super().__init__()
        self._min_size = \
            None if min_size is None else min_size if isinstance(min_size, int) else self._human_read_to_byte(min_size)
        self._max_size = \
            None if max_size is None else max_size if isinstance(max_size, int) else self._human_read_to_byte(max_size)

    def __eq__(self, size: int | str) -> Filter:
        if not (isinstance(size, int) or isinstance(size, str)):
            return NotImplemented
        self._min_size = size if isinstance(size, int) else self._human_read_to_byte(size)
        self._max_size = size if isinstance(size, int) else self._human_read_to_byte(size)
        return self
    
    def __ne__(self, size: int | str) -> Filter:
        if not (isinstance(size, int) or isinstance(size, str)):
            return NotImplemented
        return -(self == size)

    def __lt__(self, size: int | str) -> Filter:
        if not (isinstance(size, int) or isinstance(size, str)):
            return NotImplemented
        self._max_size = (size if isinstance(size, int) else self._human_read_to_byte(size)) - 1
        return self

    def __le__(self, size: int | str) -> Filter:
        if not (isinstance(size, int) or isinstance(size, str)):
            return NotImplemented
        self._max_size = size if isinstance(size, int) else self._human_read_to_byte(size)
        return self

    def __ge__(self, size: int | str) -> Filter:
        if not (isinstance(size, int) or isinstance(size, str)):
            return NotImplemented
        self._min_size = size if isinstance(size, int) else self._human_read_to_byte(size)
        return self

    def __gt__(self, size: int | str) -> Filter:
        if not (isinstance(size, int) or isinstance(size, str)):
            return NotImplemented
        self._min_size = (size if isinstance(size, int) else self._human_read_to_byte(size)) + 1
        return self

    def filter(
            self,
            root: Path,
            absolute_path: Path,
            relative_path: Path,
            depth: int,
            skipsubtree: Callable) -> bool:
        in_range: bool = False
        if absolute_path.is_file():
            size: int = os.path.getsize(absolute_path)
            min_size: int = self._min_size if self._min_size is not None else size
            max_size: int = self._max_size if self._max_size is not None else size
            in_range: bool = min_size <= size <= max_size
        return in_range if self.is_positive else not in_range


class owner(MutableFilter):

    _owners: set[str]

    def __init__(self, *owners: str) -> None:
        super().__init__()
        self._owners = set(owners)

    def __call__(self, *owners: str) -> Filter:
        return self.__class__(*owners)

    def __add__(self, other: Filter) -> Filter:
        if isinstance(other, self.__class__):
            return self.__class__(*self._owners, *other._owners)
        elif isinstance(other, Filter):
            return super().__add__(other)
        else:
            return NotImplemented

    def __eq__(self, other: str | list[str]) -> Filter:
        if isinstance(other, str):
            return self.__class__(other)
        elif isinstance(other, list):
            if any(_ for _ in other if not isinstance(_, str)):
                return NotImplemented
            return self.__class__(*other)
        return NotImplemented

    def filter(
            self,
            root: Path,
            absolute_path: Path,
            relative_path: Path,
            depth: int,
            skipsubtree: Callable) -> bool:
        in_set: bool = get_owner(absolute_path) in self._owners
        return in_set if self.is_positive else not in_set


hidden = hidden()
readonly = readonly()
executable = executable()
writeable = writeable()
owner = owner()
