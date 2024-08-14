import os
import stat
import platform
from os.path import basename
from typing import Any
from pathlib import Path


system: str = platform.system()

if system == "Windows":

    def is_hidden(path: Path | str | bytes) -> bool:
        return bool(os.stat(path).st_file_attributes & stat.FILE_ATTRIBUTE_HIDDEN)


    def is_readonly(path: Path | str | bytes) -> bool:
        return bool(os.stat(path).st_file_attributes & stat.FILE_ATTRIBUTE_READONLY)


    def is_executable(path: Any) -> Any:
        raise NotImplementedError('File\'s executable attribute detection not implemented!')


    def is_writeable(path: Any) -> Any:
        raise NotImplementedError('File\'s writeable attribute detection not implemented!')


    def get_owner(path: Any) -> Any:
        raise NotImplementedError('File\'s owner detection not implemented!')

elif system == "Linux":

    def is_hidden(path: Path | str | bytes) -> bool:
        path = os.fspath(path)
        if isinstance(path, bytes):
            prefix = b"."
        else:
            prefix = "."
        return basename(path).startswith(prefix)


    def is_readonly(path: Path | str | bytes) -> bool:
        return not os.access(path, os.W_OK)


    def is_executable(path: Path | str | bytes) -> bool:
        return os.path.isfile(path) and os.access(path, os.X_OK)


    def is_writeable(path: Path | str | bytes) -> bool:
        return \
            os.access(path, os.W_OK) if os.path.isfile(path) else \
            os.access(path, os.W_OK | os.X_OK) if os.path.isdir(path) else \
            False


    def get_owner(path: Path | str | bytes) -> str:
        return Path(path).owner()

elif system == "Darwin":

    def is_hidden(path: Path | str | bytes) -> bool:
        return bool(os.stat(path).st_flags & stat.UF_HIDDEN)


    def is_readonly(path: Path | str | bytes) -> bool:
        return not os.access(path, os.W_OK)


    def is_executable(path: Path | str | bytes) -> bool:
        return os.path.isfile(path) and os.access(path, os.X_OK)


    def is_writeable(path: Path | str | bytes) -> bool:
        return \
            os.access(path, os.W_OK) if os.path.isfile(path) else \
            os.access(path, os.W_OK | os.X_OK) if os.path.isdir(path) else \
            False


    def get_owner(path: Path | str | bytes) -> str:
        return Path(path).owner()

else:

    def is_hidden(path: Any) -> Any:
        raise NotImplementedError('File\'s hidden attribute detection not implemented!')


    def is_readonly(path: Any) -> Any:
        raise NotImplementedError('File\'s readonly attribute detection not implemented!')


    def is_executable(path: Any) -> Any:
        raise NotImplementedError('File\'s executable attribute detection not implemented!')


    def is_writeable(path: Any) -> Any:
        raise NotImplementedError('File\'s writeable attribute detection not implemented!')


    def get_owner(path: Any) -> Any:
        raise NotImplementedError('File\'s owner detection not implemented!')
