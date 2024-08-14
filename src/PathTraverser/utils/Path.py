import pathlib
import typing


def first(path: pathlib.Path) -> pathlib.Path:
    return pathlib.Path(path.parts[0])


def last(path: pathlib.Path) -> pathlib.Path:
    return pathlib.Path(path.parts[-1])


def part_count(path: pathlib.Path) -> int:
    return len(path.parts)


def starts_with(a: pathlib.Path, b: pathlib.Path) -> bool:
    if len(b.parts) > len(a.parts):
        return False
    else:
        for idx, _ in enumerate(b.parts):
            if _ != a.parts[idx]:
                return False
        return True


def __getattr__(name: str) -> typing.Any:
    if name == 'Path':
        pathlib.Path.first = property(first)
        pathlib.Path.last = property(last)
        pathlib.Path.part_count = property(part_count)
        pathlib.Path.starts_with = starts_with
        return pathlib.Path
    else:
        raise AttributeError(name)
