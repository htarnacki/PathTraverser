from pathlib import Path
from .Generic import Filter
from typing import Callable


class exclusionaryFiles(Filter):

    @property
    def is_positive(self) -> bool:
        return False

    def __neg__(self) -> Filter:
        return self

    def __pos__(self) -> Filter:
        return files

    def filter(
            self,
            root: Path,
            absolute_path: Path,
            relative_path: Path, depth: int,
            skipsubtree: Callable) -> bool:
        return not absolute_path.is_file()


class files(Filter):

    @property
    def is_positive(self) -> bool:
        return True

    def __neg__(self) -> Filter:
        return exclusionaryFiles

    def __pos__(self) -> Filter:
        return self

    def filter(self,
               root: Path,
               absolute_path: Path,
               relative_path: Path,
               depth: int,
               skipsubtree: Callable) -> bool:
        return absolute_path.is_file()


class exclusionaryDirs(Filter):

    @property
    def is_positive(self) -> bool:
        return False

    def __neg__(self) -> Filter:
        return self

    def __pos__(self) -> Filter:
        return dirs

    def filter(self,
               root: Path,
               absolute_path: Path,
               relative_path: Path,
               depth: int,
               skipsubtree: Callable) -> bool:
        return not absolute_path.is_dir()


class dirs(Filter):

    @property
    def is_positive(self) -> bool:
        return True

    def __neg__(self) -> Filter:
        return exclusionaryDirs

    def __pos__(self) -> Filter:
        return self

    def filter(self,
               root: Path,
               absolute_path: Path,
               relative_path: Path,
               depth: int,
               skipsubtree: Callable) -> bool:
        return absolute_path.is_dir()


class exclusionarySymlinks(Filter):

    @property
    def is_positive(self) -> bool:
        return False

    def __neg__(self) -> Filter:
        return self

    def __pos__(self) -> Filter:
        return symlinks

    def filter(self,
               root: Path,
               absolute_path: Path,
               relative_path: Path,
               depth: int,
               skipsubtree: Callable) -> bool:
        return not absolute_path.is_symlink()


class symlinks(Filter):

    @property
    def is_positive(self) -> bool:
        return True

    def __neg__(self) -> Filter:
        return exclusionarySymlinks

    def __pos__(self) -> Filter:
        return self

    def filter(self,
               root: Path,
               absolute_path: Path,
               relative_path: Path,
               depth: int,
               skipsubtree: Callable) -> bool:
        return absolute_path.is_symlink()


exclusionaryFiles = exclusionaryFiles()
files = files()
exclusionaryDirs = exclusionaryDirs()
dirs = dirs()
exclusionarySymlinks = exclusionarySymlinks()
symlinks = symlinks()
