'''
import json

import matplotlib.pyplot as plt
import numpy as np


with open('high_reynolds_number.json', 'r') as f:
    data = json.load(f)

fig, ax = plt.subplots(1, figsize=(16, 9))
ax.set_prop_cycle('color', plt.cm.rainbow(np.linspace(0, 1, len(data))))
for key, value in data.items():
    label = f'2^{int(np.log2(float(key)))}'
    ax.semilogy(np.linspace(0.0, 1.0, len(value['data'])), value['data'], label=label)
ax.legend(bbox_to_anchor=(1.01, 1), loc='upper left')
ax.grid()
plt.show()
'''
import json
import time

import matplotlib.pyplot as plt
import numpy as np

from burger.lang.rust import BenchRust


if __name__ == '__main__':
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
    with open('todo/high_reynolds_number.json', 'w') as f:
        json.dump({k: v.tolist() for k, v in data.items()}, f)

    fig, ax = plt.subplots(1, figsize=(16, 9))
    ax.set_prop_cycle('color', plt.cm.rainbow(np.linspace(0.0, 1.0, len(data))))
    for key, value in data.items():
        label = f'Re = 2^{int(np.log2(key))}'
        ax.plot(np.linspace(0.0, 1.0, len(value)), value, label=label, linewidth=0.7)
    ax.legend(bbox_to_anchor=(1.01, 1), loc='upper left')
    ax.grid()
    fig.savefig('high_reynolds_number.png', bbox_inches='tight', transparent=False)
    plt.show()
