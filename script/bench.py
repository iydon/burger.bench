import json

from burger import Benches


Ns = range(64, 33*64, 64)
threshold = 30.0
milliseconds = 5

memory, time = {}, {}
for name, Bench in Benches.Ts.items():
    memory[name], time[name] = {}, {}
    for N in Ns:
        bench = Bench(directory=f'todo/{name}', N=N, CFL=0.05)
        memory[name][str(N)] = bench.memory(milliseconds=milliseconds)
        result = time[name][str(N)] = bench.hyperfine(warmup=3, min_runs=9)
        if result['mean'] > threshold:
            break
with open('bench.json', 'w') as f:
    json.dump({
        'meta': Benches.version(),
        'data': {
            'memory': memory,
            'time': time,
        },
    }, f)
