__root__ = __import__('pathlib').Path(__file__).absolute().parents[1]
__import__('sys').path.append(__root__.as_posix())


import json
import time

import matplotlib.pyplot as plt
import numpy as np

from burger.lang.rust import BenchRust


if __name__ == '__main__':
    path = __root__ / 'static' / 'data' / 'reynolds.json'
    path.parent.mkdir(parents=True, exist_ok=True)

    if path.exists():
        exit()
    RE = 64
    data = {}
    for _ in range(27):
        RE *= 2
        bench = BenchRust('todo/rust', N=1024, RE=float(RE), CFL=0.05)
        tic = time.time()
        bench.run()
        toc = time.time()
        data[RE] = bench.result
        print(f'[Re={RE}] Elapsed time is {toc-tic} seconds.')
    path.write_text(json.dumps({k: v.tolist() for k, v in data.items()}))
