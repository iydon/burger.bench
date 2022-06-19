__all__ = ['BenchMpmath']


import pathlib as p
import typing as t

from ...base import Bench


class BenchMpmath(Bench):
    __template__ = p.Path(__file__).parent / 'code.py'

    dps = 33

    @classmethod
    def _version(self) -> str:
        return 'python3 --version'

    def _compile(self) -> t.List[str]:
        return ['python3 -m compileall code.py']

    def _run(self) -> str:
        return 'python3 -OO code.py'

    def _parse(self, text: str) -> t.List[float]:
        return list(map(float, text.split(',')))

    def _render(self, text: str) -> str:
        for key, value in self.parameters.items():
            text = text.replace(f'__{key}__', str(value))
        text = text.replace('__DPS__', str(self.dps))
        return text
