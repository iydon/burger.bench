import json
import pathlib as p
import sys
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
    for path in sys.argv[1:]:
        data = json.loads(p.Path(path).read_text())['data']
        # memory
        memory = data['memory']
        figure = Figure.new().set_color_number(len(memory))
        for lang, values in memory.items():
            xs, ys = [], []
            for N, value in values.items():
                xs.append(int(N))
                ys.append(value['mean'])
            figure.plot(xs, ys, label=lang.capitalize())
        figure \
            .set_label(x='N', y='Memory (KiB)') \
            .set_title('Memory Usage of Different Programming Languages') \
            .save('memory.png', legend_ncol=1)
        # time
        time = data['time']
        figure = Figure.new().set_color_number(len(time))
        for lang, values in time.items():
            xs, ys, errs = [], [], []
            for N, value in values.items():
                xs.append(int(N))
                ys.append(value['mean'])
                errs.append(value['stddev'])
            figure.errorbar(xs, ys, errs, label=lang.capitalize())
        figure \
            .set_label(x='N', y='Time (s)') \
            .set_title('Runtimes of Different Programming Languages') \
            .save('time.png', legend_ncol=1)
        plt.show()
