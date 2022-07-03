__all__ = ['BenchCpp']


import pathlib as p
import typing as t

from ...base import Bench


class BenchCppBase(Bench):
    @classmethod
    def _version(self) -> str:
        return 'g++ --version'

    def _compile(self) -> t.List[str]:
        return [f'g++ {self.__template__.name} -O3 -o cpp']

    def _run(self) -> str:
        return './cpp'

    def _parse(self, text: str) -> t.List[float]:
        text = text.strip().rstrip(',')
        return list(map(float, text.split(', ')))


BenchCpp = {}
for path in (p.Path(__file__).parent/'template').iterdir():
    BenchCpp[path.stem] = type(
        f'BenchCpp{path.stem.upper()}',
        (BenchCppBase, ),
        {'__template__': path}
    )
