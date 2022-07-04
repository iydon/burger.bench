__all__ = ['Benches']


import pathlib as p
import time
import typing as t

import numpy as np

from .base import Bench
from .lang import *


class Benches:
    Ts = {
        key[5:].lower(): values
        for key, values in globals().items()
        if key.startswith('Bench') and key[5:] and key[5].isupper() and values
    }

    def __init__(
        self,
        directory: t.Union[str, p.Path] = '.',
        N: int = 1024, RE: float = 200.0, L: float = 1.0, T: float = 2.0,
        CFL: float = 0.1,
    ) -> None:
        directory = p.Path(directory)
        self.benches = {
            lang: {
                name: Bench(directory/lang, N, RE, L, T, CFL)
                for name, Bench in Benches.items()
            } for lang, Benches in self.Ts.items()
        }

    def __getitem__(self, lang: str) -> t.Dict[str, Bench]:
        return self.benches[lang.lower()]

    @classmethod
    def version(self) -> t.Dict[str, str]:
        return {
            lang: next(iter(benches.values())).version()
            for lang, benches in self.Ts.items()
        }

    @property
    def result(self) -> t.Dict[str, t.Dict[str, t.Optional[np.ndarray]]]:
        return self._map(lambda lang, name, bench: bench.result)

    def compile(self) -> 'Benches':
        self._map(lambda lang, name, bench: bench.compile())
        return self

    def run(self) -> 'Benches':
        for benches in self.benches.values():
            for bench in benches.values():
                tic = time.time()
                bench.run()
                toc = time.time()
                print(f'[{bench}] Elapsed time is {toc-tic} seconds.')
        return self

    def reset(self) -> 'Benches':
        self._map(lambda lang, name, bench: bench.reset())
        return self

    def hyperfine(self, warmup: int = 3, min_runs: int = 9, max_runs: int = 16) -> t.Dict[str, t.Dict[str, t.Dict[str, t.Any]]]:
        return self._map(lambda lang, name, bench: bench.hyperfine(warmup, min_runs, max_runs))

    def memory(self, milliseconds: int = 5) -> t.Dict[str, t.Dict[str, t.Dict[str, float]]]:
        return self._map(lambda lang, name, bench: bench.memory(milliseconds))

    def _map(self, func: t.Callable) -> t.Dict[str, t.Dict[str, t.Any]]:
        return {
            lang: {
                name: func(lang, name, bench)
                for name, bench in benches.items()
            } for lang, benches in self.benches.items()
        }
