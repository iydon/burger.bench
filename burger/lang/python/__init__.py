__all__ = ['BenchPython']


import pathlib as p
import typing as t

from ...base import Bench


class BenchPythonBase(Bench):
    @classmethod
    def _version(self) -> str:
        return 'python3 --version'

    def _compile(self) -> t.List[str]:
        return [f'python3 -m compileall {self.__template__.name}']

    def _run(self) -> str:
        return f'python3 -OO {self.__template__.name}'

    def _parse(self, text: str) -> t.List[float]:
        return list(map(float, text.split(',')))


BenchPython = {}
for path in (p.Path(__file__).parent/'template').iterdir():
    BenchPython[path.stem] = type(
        f'BenchPython{path.stem.upper()}',
        (BenchPythonBase, ),
        {'__template__': path}
    )
