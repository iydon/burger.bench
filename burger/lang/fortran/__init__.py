__all__ = ['BenchFortran']


import pathlib as p
import typing as t

from ...base import Bench


class BenchFortran(Bench):
    __template__ = p.Path(__file__).parent / 'code.f90'

    @classmethod
    def _version(self) -> str:
        return 'gfortran --version'

    def _compile(self) -> t.List[str]:
        return ['gfortran code.f90 -O3 -o fortran']

    def _run(self) -> str:
        return './fortran'

    def _parse(self, text: str) -> t.List[float]:
        return list(map(float, text.split()))
