__all__ = ['BenchMpmath']


import pathlib as p
import typing as t

from ...base import Bench


class BenchMpmathBase(Bench):
    dps = 33

    @classmethod
    def _version(self) -> str:
        return 'python3 --version'

    def _compile(self) -> t.List[str]:
        return [f'python3 -m compileall {self.__template__.name}']

    def _run(self) -> str:
        return f'python3 -OO {self.__template__.name}'

    def _parse(self, text: str) -> t.List[float]:
        return list(map(float, text.split(',')))

    def _render(self, text: str) -> str:
        for key, value in self.parameters.items():
            text = text.replace(f'__{key}__', str(value))
        text = text.replace('__DPS__', str(self.dps))
        return text


BenchMpmath = {}
for path in (p.Path(__file__).parent/'template').iterdir():
    BenchMpmath[path.stem] = type(
        f'BenchMpmath{path.stem.upper()}',
        (BenchMpmathBase, ),
        {'__template__': path}
    )

