__all__ = ['BenchPython']


import pathlib as p
import typing as t

from ...base import Bench


class BenchPython(Bench):
    __template__ = p.Path(__file__).parent / 'code.py'

    @classmethod
    def _version(self) -> str:
        return 'python3 --version'

    def _compile(self) -> t.List[str]:
        return ['python3 -m compileall code.py']

    def _run(self) -> str:
        return 'python3 -OO code.py'

    def _parse(self, text: str) -> t.List[float]:
        return list(map(float, text.split(',')))
