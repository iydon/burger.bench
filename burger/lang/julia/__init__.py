__all__ = ['BenchJulia']


import pathlib as p
import typing as t

from ...base import Bench


class BenchJuliaBase(Bench):
    @classmethod
    def _version(self) -> str:
        return 'julia --version'

    def _compile(self) -> t.List[str]:
        return []

    def _run(self) -> str:
        return f'julia -O3 {self.__template__.name}'

    def _parse(self, text: str) -> t.List[float]:
        text = text.replace('[', '').replace(']', '')
        return list(map(float, text.split()))


BenchJulia = {}
for path in (p.Path(__file__).parent/'template').iterdir():
    BenchJulia[path.stem] = type(
        f'BenchJulia{path.stem.upper()}',
        (BenchJuliaBase, ),
        {'__template__': path}
    )
