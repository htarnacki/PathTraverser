from .Generic import Filter, MutableFilter
from pathlib import Path
from typing import  Callable
from inspect import Parameter, signature
from types import FunctionType, MappingProxyType


class call(MutableFilter):

    _callables: tuple[Callable]
    _callables_signatures: list[None | dict[str, bool]]

    @staticmethod
    def _get_params_signature_for_callable(callable: Callable) -> None | dict[str, bool]:
        if not isinstance(callable, FunctionType):
            callable = callable.__call__
        params: MappingProxyType[str, Parameter] = signature(callable).parameters
        result: dict[str, bool] = {
            'rel': 'rel' in params,
            'root': 'root' in params,
            'depth': 'depth' in params,
            'skipsubtree': 'skipsubtree' in params
        }
        return result if any(_ for _ in result.values()) else None

    def __init__(self, *callables: Callable) -> None:
        super().__init__()
        self._callables = callables
        self._callables_signatures = []
        for _ in self._callables:
            if not callable(_):
                raise TypeError('Parameter is not callable!')
            self._callables_signatures.append(self._get_params_signature_for_callable(_))

    def __call__(self, *callables: Callable) -> Filter:
        return self.__class__(*callables)

    def filter(
            self,
            root: Path,
            absolute_path: Path,
            relative_path: Path,
            depth: int,
            skipsubtree: Callable) -> bool:
        result: bool = True
        for idx, callable in enumerate(self._callables):
            kwargs = \
                {_: (
                        relative_path if _ == 'rel' else 
                        root if _ == 'root' else 
                        depth if _ == 'depth' else
                        skipsubtree if _ == 'skipsubtree' else
                        None
                    ) for _ in self._callables_signatures[idx].keys() if self._callables_signatures[idx][_]
                } if self._callables_signatures[idx] else \
                dict()
            if not callable(absolute_path, **kwargs):
                result = False
                break
        return result if self.is_positive else not result


call = call()
