__root__ = __import__('pathlib').Path(__file__).absolute().parents[1]
__import__('sys').path.append(__root__.as_posix())


import functools as f
import json

import numpy as np

from burger import Benches


if __name__ == '__main__':
    dN = 64
    threshold = 30.0
    milliseconds = 5
    path = __root__ / 'static' / 'data' / 'bench.json'
    path.parent.mkdir(parents=True, exist_ok=True)

    if path.exists():
        exit()
    names = f.reduce(set.intersection, map(set, Benches.Ts.values()))
    memory, time = {}, {}
    for lang, Bs in Benches.Ts.items():
        memory[lang], time[lang] = {}, {}
        for name in names:
            memory[lang][name], time[lang][name] = {}, {}
            N = 0
            while True:
                N += dN
                bench = Bs[name](directory=f'todo/{lang}', N=N, CFL=0.05).run()
                if np.isnan(bench.result).any():
                    break
                memory[lang][name][str(N)] = bench.memory(milliseconds=milliseconds)
                result = time[lang][name][str(N)] = bench.hyperfine(warmup=3, min_runs=9, max_runs=16)
                if result['execute']['mean'] > threshold:
                    break
    path.write_text(
        json.dumps({
            'meta': Benches.version(),
            'data': {
                'memory': memory,
                'time': time,
            },
        })
    )
