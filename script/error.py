__root__ = __import__('pathlib').Path(__file__).absolute().parents[1]
__import__('sys').path.append(__root__.as_posix())


import itertools as it

import numpy as np
import pandas as pd

from burger import Benches


if __name__ == '__main__':
    rmse = lambda x, y: np.sqrt(np.mean((x-y)**2))
    bs = Benches('todo', N=256, CFL=0.05) \
        .run()
    keys = list(map(str.capitalize, Benches.Ts.keys()))
    error = pd.DataFrame(0.0, index=keys, columns=keys)
    for key1, key2 in it.combinations(keys, 2):
        error.loc[key1, key2] = error.loc[key2, key1] = \
            np.sqrt(np.mean((bs[key1].result-bs[key2].result)**2))
    error.to_csv(__root__/'static'/'data'/'error.csv')
