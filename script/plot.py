__root__ = __import__('pathlib').Path(__file__).absolute().parents[1]
__import__('sys').path.append(__root__.as_posix())
__import__('warnings').filterwarnings('ignore')


import json
import pathlib as p
import typing as t

import matplotlib.pyplot as plt
import numpy as np


class Figure:
    def __init__(self, figsize: t.Optional[t.Tuple[int, int]] = None) -> None:
        self._fig, self._ax = plt.subplots(1, figsize=(figsize or (16, 9)))

    @classmethod
    def new(cls, **kwargs) -> 'Figure':
        return cls(**kwargs)

    def set_color_number(self, number: int) -> 'Figure':
        self._ax.set_prop_cycle('color', plt.cm.rainbow(np.linspace(0, 1, number)))
        return self

    def set_label(self, x: t.Optional[str] = None, y: t.Optional[str] = None) -> 'Figure':
        if x is not None:
            self._ax.set_xlabel(x)
        if y is not None:
            self._ax.set_ylabel(y)
        return self

    def set_title(self, title: str) -> 'Figure':
        self._ax.set_title(title)
        return self

    def plot(self, x: t.Any, y: t.Any, label: str, **kwargs) -> 'Figure':
        kwargs = {
            'marker': 'o', 'markersize': 7, 'label': label,
            **kwargs,
        }
        self._ax.plot(x, y, **kwargs)
        return self

    def semilogy(self, x: t.Any, y: t.Any, label: str, **kwargs) -> 'Figure':
        kwargs = {
            'marker': 'o', 'markersize': 7, 'label': label,
            **kwargs,
        }
        self._ax.semilogy(x, y, **kwargs)
        return self

    def scatter(self, x: t.Any, y: t.Any, label: str, **kwargs) -> 'Figure':
        kwargs = {'label': label, **kwargs}
        self._ax.scatter(x, y, **kwargs)
        return self

    def errorbar(self, x: t.Any, y: t.Any, yerr: t.Any, label: str, **kwargs) -> 'Figure':
        kwargs = {'label': label, **kwargs}
        self._ax.errorbar(x, y, yerr=yerr, **kwargs)
        return self

    def save(self, path: str, legend_ncol: int = 0, grid: bool = True, transparent: bool = False) -> 'Figure':
        if legend_ncol:
            self._ax.legend(bbox_to_anchor=(1.01, 1), loc='upper left', borderaxespad=0, ncol=legend_ncol)
        if grid:
            self._ax.grid()
        self._fig.savefig(path, bbox_inches='tight', transparent=transparent)
        return self


if __name__ == '__main__':
    dir_data = __root__ / 'static' / 'data'
    dir_data.mkdir(parents=True, exist_ok=True)
    dir_image = __root__ / 'static' / 'image'
    dir_image.mkdir(parents=True, exist_ok=True)
    path_bench = dir_data / 'bench.json'
    path_reynolds = dir_data / 'reynolds.json'

    if path_bench.exists():
        # bench
        bench = json.loads(p.Path(path_bench).read_text())
        meta, data = bench['meta'], bench['data']
        for lang, version in meta.items():
            print(f'{lang.capitalize()}: {version.splitlines()[0]}')
        names = {'fdm', 'fvm'}
        ## memory
        for name in names:
            dir_memory = dir_image / 'memory' / name
            dir_memory.mkdir(parents=True, exist_ok=True)
            memory = {k: v[name] for k, v in data['memory'].items()}
            for field in next(iter(next(iter(memory.values())).values())):
                figure = Figure.new().set_color_number(len(memory))
                for lang, values in memory.items():
                    xs, ys = [], []
                    for N, value in values.items():
                        xs.append(int(N))
                        ys.append(value[field]['mean']*1000/2**20)
                    figure.semilogy(xs, ys, label=lang.capitalize())
                figure \
                    .set_label(x='N', y='Memory (MiB)') \
                    .set_title(f'Memory Usage of Different Programming Languages ({field})') \
                    .save(dir_memory/f'{field}.png', legend_ncol=1)
        ## time
        for name in names:
            dir_time = dir_image / 'time' / name
            dir_time.mkdir(parents=True, exist_ok=True)
            time = {k: v[name] for k, v in data['time'].items()}
            for key, title in {('compile', 'Compile Time'), ('execute', 'Runtime')}:
                figure = Figure.new().set_color_number(len(time))
                for lang, values in time.items():
                    xs, ys, errs = [], [], []
                    for N, value in values.items():
                        xs.append(int(N))
                        ys.append(value[key]['mean'])
                        errs.append(value[key]['stddev'])
                    figure.errorbar(xs, ys, errs, label=lang.capitalize())
                figure \
                    .set_label(x='N', y='Time (s)') \
                    .set_title(f'{title} of Different Programming Languages') \
                    .save(dir_time/f'{key}.png', legend_ncol=1)

    if path_reynolds.exists():
        # reynolds
        reynolds = json.loads(p.Path(path_reynolds).read_text())
        figure = Figure.new().set_color_number(len(reynolds))
        for key, value in reynolds.items():
            label = f'Re = 2^{int(np.log2(float(key)))}'
            figure.scatter(np.linspace(0.0, 1.0, len(value)), value, s=5, label=label)
        figure \
            .set_label(x='N', y='Time (s)') \
            .save(dir_image/'reynolds.png', legend_ncol=1)
