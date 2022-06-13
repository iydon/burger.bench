__all__ = ['Benches']


import pathlib as p
import typing as t

import numpy as np

from .base import Bench
from .lang import *


class Benches:
    Ts = {
        key[5:].lower(): value
        for key, value in globals().items()
        if key.startswith('Bench') and key[5:] and key[5].isupper()
    }

    def __init__(
        self,
        directory: t.Union[str, p.Path] = '.',
        N: int = 1024, RE: float = 200.0, L: float = 1.0, T: float = 2.0,
        CFL: float = 0.1,
    ) -> None:
        directory = p.Path(directory)
        self.benches = {
            key: Value(directory/key, N, RE, L, T, CFL)
            for key, Value in self.Ts.items()
        }

    def __getitem__(self, key: str) -> Bench:
        return self.benches[key.lower()]

    @classmethod
    def version(self) -> t.Dict[str, str]:
        return {
            key: value.version()
            for key, value in self.Ts.items()
        }

    @property
    def result(self) -> t.Dict[str, t.Optional[np.ndarray]]:
        return {
            key: value.result
            for key, value in self.benches.items()
        }

    def compile(self) -> 'Benches':
        for bench in self.benches.values():
            bench.compile()
        return self

    def run(self) -> 'Benches':
        for bench in self.benches.values():
            bench.run()
        return self

    def reset(self) -> 'Benches':
        for bench in self.benches.values():
            bench.reset()
        return self

    def hyperfine(self, warmup: int = 3, min_runs: int = 9) -> t.Dict[str, t.Dict[str, t.Any]]:
        return {
            key: value.hyperfine(warmup, min_runs)
            for key, value in self.benches.items()
        }

    def memory(self, milliseconds: int = 5) -> t.Dict[str, t.Dict[str, float]]:
        return {
            key: value.memory(milliseconds)
            for key, value in self.benches.items()
        }
