import json

from burger import Benches


Ns = range(64, 33*64, 64)
threshold = 30.0

data = {}
for name, Bench in Benches.Ts.items():
    data[name] = {}
    for N in Ns:
        bench = Bench(directory=f'todo/{name}', N=N, CFL=0.05)
        result = data[name][str(N)] = bench.hyperfine(warmup=3, min_runs=9)
        if result['mean'] > threshold:
            break
with open('bench.json', 'w') as f:
    json.dump({'meta': Benches.version(), 'data': data}, f)
