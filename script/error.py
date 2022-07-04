__root__ = __import__('pathlib').Path(__file__).absolute().parents[1]
__import__('sys').path.append(__root__.as_posix())


import functools as f
import itertools as it

import numpy as np
import pandas as pd

from burger import Benches
from burger.extra import BenchMpmath


def rmse(x: np.ndarray, y: np.ndarray) -> float:
    return np.sqrt(np.mean((x-y)**2))


if __name__ == '__main__':
    directory = __root__ / 'static' / 'data' / 'error'
    directory.mkdir(parents=True, exist_ok=True)

    for B in BenchMpmath.values():
        B.dps = 33  # float64
    Benches.Ts['mpmath'] = BenchMpmath
    bs = Benches('todo', N=128, CFL=0.1) \
        .compile() \
        .run()
    keys = list(map(str.capitalize, Benches.Ts.keys()))
    for name in f.reduce(set.intersection, map(set, Benches.Ts.values())):
        error = pd.DataFrame(0.0, index=keys, columns=keys)
        for key1, key2 in it.combinations(keys, 2):
            error.loc[key1, key2] = error.loc[key2, key1] = \
                rmse(bs[key1][name].result, bs[key2][name].result)
        error.to_csv(directory/f'{name}.csv')
        print(name)
        print(error)
