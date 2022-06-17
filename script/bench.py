__root__ = __import__('pathlib').Path(__file__).absolute().parents[1]
__import__('sys').path.append(__root__.as_posix())


import json

import numpy as np

from burger import Benches


dN = 64
threshold = 30.0
milliseconds = 5
directory = __root__ / 'static' / 'data'
directory.mkdir(parents=True, exist_ok=True)
path = directory / 'bench.json'

if path.exists():
    exit()
memory, time = {}, {}
for name, Bench in Benches.Ts.items():
    memory[name], time[name] = {}, {}
    N = 0
    while True:
        N += dN
        bench = Bench(directory=f'todo/{name}', N=N, CFL=0.05).run()
        if np.isnan(bench.result).any():
            break
        memory[name][str(N)] = bench.memory(milliseconds=milliseconds)
        result = time[name][str(N)] = bench.hyperfine(warmup=1, min_runs=7)
        if result['mean'] > threshold:
            break
with open(directory/'bench.json', 'w') as f:
    json.dump({
        'meta': Benches.version(),
        'data': {
            'memory': memory,
            'time': time,
        },
    }, f)
