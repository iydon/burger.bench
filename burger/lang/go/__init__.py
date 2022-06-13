__all__ = ['BenchGo']


import pathlib as p
import typing as t

from ...base import Bench


class BenchGo(Bench):
    __template__ = p.Path(__file__).parent / 'code.go'

    @classmethod
    def _version(self) -> str:
        return 'go version'

    def _compile(self) -> t.List[str]:
        return ['go build -o go -ldflags "-s -w"']

    def _run(self) -> str:
        return './go'

    def _parse(self, text: str) -> t.List[float]:
        text = text.replace('[', '').replace(']', '')
        return list(map(float, text.split()))
