__all__ = ['BenchGo']


import pathlib as p
import typing as t

from ...base import Bench


class BenchGoBase(Bench):
    @classmethod
    def _version(self) -> str:
        return 'go version'

    def _compile(self) -> t.List[str]:
        return [f'go build -o {self.__template__.stem} -ldflags "-s -w" {self.__template__.name}']

    def _run(self) -> str:
        return f'./{self.__template__.stem}'

    def _parse(self, text: str) -> t.List[float]:
        text = text.replace('[', '').replace(']', '')
        return list(map(float, text.split()))


BenchGo = {}
for path in (p.Path(__file__).parent/'template').iterdir():
    BenchGo[path.stem] = type(
        f'BenchGo{path.stem.upper()}',
        (BenchGoBase, ),
        {'__template__': path}
    )
