__all__ = ['BenchJulia']


import pathlib as p
import typing as t

from ...base import Bench


class BenchJulia(Bench):
    __template__ = p.Path(__file__).parent / 'code.jl'

    def _compile(self) -> t.List[str]:
        return []

    def _run(self) -> str:
        return 'julia -O3 code.jl'

    def _parse(self, text: str) -> t.List[float]:
        text = text.replace('[', '').replace(']', '')
        return list(map(float, text.split()))
