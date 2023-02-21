import os
import re
from inspect import signature
from pathlib import Path
from enum import Enum
from types import FunctionType
from typing import Union, Callable, List, Set, Iterator, Dict


class PathTypes(Enum):
    ANY: str = 'any'
    FILE: str = 'file'  # file or link to file
    LINK: str = 'link'  # link to file or directory
    DIRECTORY: str = 'directory'  # directory or link to directory


def _get_params_signature_for_callable(callable: Callable) -> Union[None, Dict[str, bool]]:
    if callable:
        if not isinstance(callable, FunctionType):
            callable = callable.__call__
        params = signature(callable).parameters
        return {
            'rel': 'rel' in params,
            'root': 'root' in params,
            'depth': 'depth' in params
        }


class Traverser:

    # private members
    _root: Path
    _depth: int
    _pathtype: PathTypes
    _mindepth: int
    _maxdepth: int
    _pathfilter: Callable
    _namefilter: Union[re.Pattern, str]
    _extfilter: str
    _exclude_pathfilter: Callable
    _exclude_namefilter: Union[re.Pattern, str]
    _exclude_extfilter: str
    _followlinks: bool
    _onerror: Callable
    _iterator: Iterator
    _dirpath: str
    _dirnames: List[str]
    _filenames: List[str]
    _results: Set[Path]
    _pathfilter_signature: Dict[str, bool]
    _exclude_pathfilter_signature: Dict[str, bool]

    def __init__(
        self,
        root: Union[Path, str],
        pathtype: PathTypes = PathTypes.ANY,
        mindepth: int = 0,
        maxdepth: int = None,
        pathfilter: Callable = None,
        namefilter: Union[re.Pattern, str] = None,
        extfilter: str = None,
        exclude_pathfilter: Callable = None,
        exclude_namefilter: Union[re.Pattern, str] = None,
        exclude_extfilter: str = None,
        followlinks: bool = True,
        onerror: Callable = None
    ):
        self._root = Path(root)
        if not self._root.is_absolute():
            self._root = Path.cwd() / self._root
        self._pathtype = pathtype
        self._mindepth = mindepth
        self._maxdepth = maxdepth
        self._pathfilter = pathfilter
        self._namefilter = namefilter
        self._extfilter = extfilter
        self._exclude_pathfilter = exclude_pathfilter
        self._exclude_namefilter = exclude_namefilter
        self._exclude_extfilter = exclude_extfilter
        self._followlinks = followlinks
        self._onerror = onerror
        # analyze callable filters
        self._pathfilter_signature = _get_params_signature_for_callable(pathfilter)
        self._exclude_pathfilter_signature = _get_params_signature_for_callable(exclude_pathfilter)

    @property
    def root(self) -> Path:
        return self._root

    @property
    def depth(self) -> int:
        return self._depth

    @property
    def pathtype(self) -> PathTypes:
        return self._pathtype

    @property
    def mindepth(self) -> int:
        return self._mindepth

    @property
    def maxdepth(self) -> int:
        return self._maxdepth

    @property
    def pathfilter(self) -> Callable:
        return self._pathfilter

    @property
    def namefilter(self) -> Union[re.Pattern, str]:
        return self._namefilter

    @property
    def extfilter(self) -> str:
        return self._extfilter

    @property
    def exclude_pathfilter(self) -> Callable:
        return self._exclude_pathfilter

    @property
    def exclude_namefilter(self) -> Union[re.Pattern, str]:
        return self._exclude_namefilter

    @property
    def exclude_extfilter(self) -> str:
        return self._exclude_extfilter

    @property
    def followlinks(self) -> bool:
        return self._followlinks

    @property
    def onerror(self) -> Callable:
        return self._onerror

    def __enter__(self) -> 'Traverser':
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    def __iter__(self) -> 'Traverser':
        self._iterator = os.walk(
            self.root,
            topdown=True,
            followlinks=self.followlinks,
            onerror=self.onerror)
        self._dirpath = None
        self._dirnames = None
        self._filenames = None
        self._results = None
        self._depth = None
        return self

    def __next__(self) -> 'Path':
        if not self._results or len(self._results) < 1:
            while True:
                self._dirpath, self._dirnames, self._filenames = next(self._iterator)
                # calculate some usefull values
                dirpath = Path(self._dirpath)
                rel_dirpath = dirpath.relative_to(self.root)
                currdepth = \
                    0 if rel_dirpath.name == '.' else \
                    len(rel_dirpath.parts)
                # skip this iteration if insufficient depth level
                if self.mindepth and self.mindepth > currdepth:
                    continue
                # collect subpaths for current dirpath taking their types into consideration
                paths = \
                    {*self._dirnames} if self.pathtype == PathTypes.DIRECTORY else \
                    {*self._filenames} if self.pathtype == PathTypes.FILE else \
                    {*self._dirnames, *self._filenames}
                # apply "link" file type filter to collected subpaths
                if self.pathtype == PathTypes.LINK:
                    for _ in [*paths]:
                        _ = dirpath / _
                        if not _.is_symlink():
                            paths.remove(_.name)
                # apply exclude filters
                if self.exclude_namefilter:
                    # apply exclude name filter
                    for _ in [*paths]:
                        if (
                            (
                                isinstance(self.exclude_namefilter, re.Pattern)
                                and re.match(self.exclude_namefilter, _)
                            )
                            or (
                                isinstance(self.exclude_namefilter, str)
                                and _ == self.exclude_namefilter
                            )
                        ):
                            paths.remove(_)
                if self.exclude_extfilter:
                    # apply exclude extension filter
                    for _ in [*paths]:
                        _ = dirpath / _
                        if _.is_file() and _.suffix == f'.{self.exclude_extfilter}':
                            paths.remove(_.name)
                if self.exclude_pathfilter:
                    # apply exclude path filter
                    for _ in [*paths]:
                        kwargs = dict()
                        if self._exclude_pathfilter_signature['rel']:
                            rel = Path(_) if rel_dirpath.name == '.' else rel_dirpath / _
                            kwargs['rel'] = rel
                        if self._exclude_pathfilter_signature['root']:
                            kwargs['root'] = self.root
                        if self._exclude_pathfilter_signature['depth']:
                            kwargs['depth'] = currdepth
                        if (self.exclude_pathfilter(dirpath / _, **kwargs)):
                            paths.remove(_)
                # apply include filters
                if self.namefilter:
                    # apply name filter
                    for _ in [*paths]:
                        if not (
                            (
                                isinstance(self.namefilter, re.Pattern)
                                and re.match(self.namefilter, _)
                            )
                            or (
                                isinstance(self.namefilter, str)
                                and _ == self.namefilter
                            )
                        ):
                            paths.remove(_)
                if self.extfilter:
                    # apply extension filter. This automatically removes directories from results
                    for _ in [*paths]:
                        _ = dirpath / _
                        if not (_.is_file() and _.suffix == f'.{self.extfilter}'):
                            paths.remove(_.name)
                if self.pathfilter:
                    # apply path filter
                    for _ in [*paths]:
                        kwargs = dict()
                        if self._pathfilter_signature['rel']:
                            rel = Path(_) if rel_dirpath.name == '.' else rel_dirpath / _
                            kwargs['rel'] = rel
                        if self._pathfilter_signature['root']:
                            kwargs['root'] = self.root
                        if self._pathfilter_signature['depth']:
                            kwargs['depth'] = currdepth
                        if not (self.pathfilter(dirpath / _, **kwargs)):
                            paths.remove(_)
                # check current depth and decide if we are allowed to iterate deeper
                if self.maxdepth is not None and currdepth >= self.maxdepth:
                    self._dirnames.clear()
                # break if finally there are some results ready to return
                if len(paths) > 0:
                    self._results = paths
                    self._depth = currdepth
                    break
        return Path(self._dirpath) / self._results.pop()

    def skipsubtree(self, *names: Union[Path, str]) -> 'Traverser':
        if self._dirnames:
            for name in names:
                name = \
                    name if isinstance(name, str) else \
                    name.name if isinstance(name, Path) else \
                    str(name)
                if name in self._dirnames:
                    self._dirnames.remove(name)
        return self
