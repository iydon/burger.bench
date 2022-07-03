__all__ = ['BenchC']


import pathlib as p
import typing as t

from ...base import Bench


class BenchCBase(Bench):
    @classmethod
    def _version(self) -> str:
        return 'gcc --version'

    def _compile(self) -> t.List[str]:
        return [f'gcc {self.__template__.name} -lm -O3 -o {self.__template__.stem}']

    def _run(self) -> str:
        return f'./{self.__template__.stem}'

    def _parse(self, text: str) -> t.List[float]:
        text = text.strip().rstrip(',')
        return list(map(float, text.split(', ')))


BenchC = {}
for path in (p.Path(__file__).parent/'template').iterdir():
    BenchC[path.stem] = type(
        f'BenchC{path.stem.upper()}',
        (BenchCBase, ),
        {'__template__': path}
    )
