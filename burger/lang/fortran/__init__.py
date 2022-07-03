__all__ = ['BenchFortran']


import pathlib as p
import typing as t

from ...base import Bench


class BenchFortranBase(Bench):
    @classmethod
    def _version(self) -> str:
        return 'gfortran --version'

    def _compile(self) -> t.List[str]:
        return [f'gfortran {self.__template__.name} -O3 -o {self.__template__.stem}']

    def _run(self) -> str:
        return f'./{self.__template__.stem}'

    def _parse(self, text: str) -> t.List[float]:
        return list(map(float, text.split()))


BenchFortran = {}
for path in (p.Path(__file__).parent/'template').iterdir():
    BenchFortran[path.stem] = type(
        f'BenchFortran{path.stem.upper()}',
        (BenchFortranBase, ),
        {'__template__': path}
    )
