import json
import pathlib as p
import sys

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


sns.set_theme()


if __name__ == '__main__':
    for path in sys.argv[1:]:
        data = json.loads(p.Path(path).read_text())
        dfs = [None] * len(data)
        for ith, (lang, values) in enumerate(data.items()):
            xs, ys = [], []
            for N, value in values.items():
                xs += [int(N)] * len(value['times'])
                ys += value['times']
            dfs[ith] = pd.DataFrame({'N': xs, 'Time (s)': ys, 'Language': lang.capitalize()})
    sns.lineplot(data=pd.concat(dfs), x='N', y='Time (s)', hue='Language')
    plt.show()
