__all__ = ['BenchRust']


import pathlib as p
import typing as t

from ...base import Bench


class BenchRustBase(Bench):
    @classmethod
    def _version(self) -> str:
        return 'rustc --version'

    def _compile(self) -> t.List[str]:
        return [f'rustc {self.__template__.name} -C opt-level=3 -o rust']

    def _run(self) -> str:
        return './rust'

    def _parse(self, text: str) -> t.List[float]:
        text = text.replace('[', '').replace(']', '')
        return list(map(float, text.split(', ')))


BenchRust = {}
for path in (p.Path(__file__).parent/'template').iterdir():
    BenchRust[path.stem] = type(
        f'BenchRust{path.stem.upper()}',
        (BenchRustBase, ),
        {'__template__': path}
    )
