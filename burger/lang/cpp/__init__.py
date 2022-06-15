__all__ = ['BenchCpp']


import pathlib as p
import typing as t

from ...base import Bench


class BenchCpp(Bench):
    __template__ = p.Path(__file__).parent / 'code.cpp'

    @classmethod
    def _version(self) -> str:
        return 'g++ --version'

    def _compile(self) -> t.List[str]:
        return ['g++ code.cpp -O3 -o cpp']

    def _run(self) -> str:
        return './cpp'

    def _parse(self, text: str) -> t.List[float]:
        text = text.strip().rstrip(',')
        return list(map(float, text.split(', ')))
