import os
from pathlib import Path
from typing import Union, Callable, Iterator, Self
from collections.abc import Iterable as ABCIterable, Iterator as ABCIterator
from .filters import Filter, files, dirs, symlinks
from itertools import chain
from contextlib import suppress


class Iterator(ABCIterator):
    _root: Path = None
    _filters: tuple[Filter] = None
    _iterator: Iterator[tuple] = None
    _dirpath: Path = None
    _rel_dirpath: Path = None
    _dirnames: list[str] = None
    _items: Iterator[str] = []
    _depth: int = None
    _on_each: Callable = None
    _on_file: Callable = None
    _on_dir: Callable = None
    _on_symlink: Callable = None

    def __init__(
            self,
            root: Path | str,
            *filters: Filter,
            topdown: bool = True,
            followlinks: bool = False,
            onerror: Callable = None,
            on_each: Callable = None,
            on_file: Callable = None,
            on_dir: Callable = None,
            on_symlink: Callable = None) -> None:
        self._root = Path(root)
        self._filters = filters
        self._iterator = os.walk(root, topdown=topdown, followlinks=followlinks, onerror=onerror)
        self._on_each = on_each
        self._on_file = on_file
        self._on_dir = on_dir
        self._on_symlink = on_symlink

    @property
    def root(self) -> Path:
        return self._root

    @property
    def depth(self) -> int:
        return self._depth

    def __call__(self, *filters: Filter) -> Iterator:
        self._filters = (*self._filters, *filters)
        return self

    def __enter__(self) -> 'Iterator':
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        pass

    def __next__(self) -> 'Path':
        while item := next(chain(self._items, self._iterator), None):
            if isinstance(item, tuple):
                self._dirpath, self._dirnames, filenames = item
                self._dirpath = Path(self._dirpath)
                self._rel_dirpath: Path = self._dirpath.relative_to(self._root)
                self._depth: int = 0 if self._rel_dirpath.name == '.' else len(self._rel_dirpath.parts)
                self._items = iter([*self._dirnames, *filenames])
                return self.__next__()
            else:
                item_path: Path = self._dirpath / item
                item_rel_path: Path = self._rel_dirpath / item
                for filter in self._filters:
                    if not filter.filter(self._root, item_path, item_rel_path, self._depth, self.skipsubtree):
                        break
                else:
                    if self._on_each:
                        self._on_each(item_path)
                    if self._on_file and item_path.is_file():
                        self._on_file(item_path)
                    if self._on_dir and item_path.is_dir():
                        self._on_dir(item_path)
                    if self._on_symlink and item_path.is_symlink():
                        self._on_symlink(item_path)
                    return item_path
        else:
            raise StopIteration()

    def on_each(self, executable: Callable) -> 'Iterator':
        self._on_each = executable
        return self

    def on_file(self, executable: Callable) -> 'Iterator':
        self._on_file = executable
        return self

    def on_dir(self, executable: Callable) -> 'Iterator':
        self._on_dir = executable
        return self

    def on_symlink(self, executable: Callable) -> 'Iterator':
        self._on_symlink = executable
        return self

    def get(self) -> list[Path]:
        return list(self)

    def skipsubtree(self, *names: Union[Path, str]) -> Self:
        if self._dirnames:
            for name in names:
                name: str = \
                    name if isinstance(name, str) else \
                    name.name if isinstance(name, Path) else \
                    str(name)
                with suppress(ValueError):
                    self._dirnames.remove(name)
        return self


class Traverser(ABCIterable):

    _root: Path = None
    _filters: tuple[Filter] = None
    _topdown: bool = None
    _followlinks: bool = None
    _onerror: Callable = None
    _on_each: Callable = None
    _on_file: Callable = None
    _on_dir: Callable = None
    _on_symlink: Callable = None

    def __init__(
        self,
        root: Path | str = None,
        *filters: Filter,
        topdown: bool = True,
        followlinks: bool = True,
        onerror: Callable = None,
        on_each: Callable = None,
        on_file: Callable = None,
        on_dir: Callable = None,
        on_symlink: Callable = None
    ) -> None:
        if root is None:
            self._root = Path.cwd()
        elif isinstance(root, Filter):
            self._root = Path.cwd()
            filters = tuple([root, *filters])
        else:
            self._root = Path(root)
        if not self._root.is_absolute():
            self._root = Path.cwd() / self._root
        self._filters = filters
        self._topdown = topdown
        self._followlinks = followlinks
        self._onerror = onerror
        self._on_each = on_each
        self._on_file = on_file
        self._on_dir = on_dir
        self._on_symlink = on_symlink

    @property
    def root(self) -> Path:
        return self._root

    def filter(self, *filters: Filter) -> Iterator:
        return Iterator(
            self.root,
            *(*self._filters, *filters),
            topdown=self._topdown,
            followlinks=self._followlinks,
            onerror=self._onerror,
            on_each=self._on_each,
            on_file=self._on_file,
            on_dir=self._on_dir,
            on_symlink=self._on_symlink
        )

    @property
    def files(self, *filters: Filter) -> Iterator:
        return Iterator(
            self.root,
            *(*self._filters, files, *filters),
            topdown=self._topdown,
            followlinks=self._followlinks,
            onerror=self._onerror,
            on_each=self._on_each,
            on_file=self._on_file,
            on_dir=self._on_dir,
            on_symlink=self._on_symlink
        )

    @property
    def dirs(self, *filters: Filter) -> Iterator:
        return Iterator(
            self.root,
            *(*self._filters, dirs, *filters),
            topdown=self._topdown,
            followlinks=self._followlinks,
            onerror=self._onerror,
            on_each=self._on_each,
            on_file=self._on_file,
            on_dir=self._on_dir,
            on_symlink=self._on_symlink
        )

    @property
    def symlinks(self, *filters: Filter) -> Iterator:
        return Iterator(
            self.root,
            *(*self._filters, symlinks, *filters),
            topdown=self._topdown,
            followlinks=self._followlinks,
            onerror=self._onerror,
            on_each=self._on_each,
            on_file=self._on_file,
            on_dir=self._on_dir,
            on_symlink=self._on_symlink
        )

    def __enter__(self) -> 'Traverser':
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        pass

    def __iter__(self) -> Iterator:
        return Iterator(
            self.root,
            *self._filters,
            topdown=self._topdown,
            followlinks=self._followlinks,
            onerror=self._onerror,
            on_each=self._on_each,
            on_file=self._on_file,
            on_dir=self._on_dir,
            on_symlink=self._on_symlink
        )
    
    def iter(self) -> Iterator:
        return iter(self)

    def on_each(self, executable: Callable) -> 'Iterator':
        self._on_each = executable
        return self

    def on_file(self, executable: Callable) -> 'Iterator':
        self._on_file = executable
        return self

    def on_dir(self, executable: Callable) -> 'Iterator':
        self._on_dir = executable
        return self

    def on_symlink(self, executable: Callable) -> 'Iterator':
        self._on_symlink = executable
        return self

    def get(self) -> list[Path]:
        return list(iter(self))
