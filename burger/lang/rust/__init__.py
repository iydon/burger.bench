__all__ = ['BenchRust']


import pathlib as p
import typing as t

from ...base import Bench


class BenchRust(Bench):
    __template__ = p.Path(__file__).parent / 'code.rs'

    def _compile(self) -> t.List[str]:
        return ['rustc code.rs -C opt-level=3 -o rust']

    def _run(self) -> str:
        return './rust'

    def _parse(self, text: str) -> t.List[float]:
        text = text.replace('[', '').replace(']', '')
        return list(map(float, text.split(', ')))
