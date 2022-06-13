__all__ = ['BenchC']


import pathlib as p
import typing as t

from ...base import Bench


class BenchC(Bench):
    __template__ = p.Path(__file__).parent / 'code.c'

    @classmethod
    def _version(self) -> str:
        return 'gcc --version'

    def _compile(self) -> t.List[str]:
        return ['gcc code.c -lm -O3 -o c']

    def _run(self) -> str:
        return './c'

    def _parse(self, text: str) -> t.List[float]:
        text = text.strip().rstrip(',')
        return list(map(float, text.split(', ')))
