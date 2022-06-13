import json

import numpy as np

from burger import Benches


Ns = np.arange(64, 33*64, 64)
threshold = 15.0

data = {}
for name, Bench in Benches.Ts.items():
    data[name] = {}
    for N in Ns:
        bench = Bench(directory=f'todo/{name}', N=N, CFL=0.05)
        result = data[name][str(N)] = bench.hyperfine()
        if result['mean'] > threshold:
            break
with open('bench.json', 'w') as f:
    json.dump({'meta': Benches.version(), 'data': data}, f)
