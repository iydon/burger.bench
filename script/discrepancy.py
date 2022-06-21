# https://stackoverflow.com/questions/2757424/discrepancy-between-the-values-computed-by-fortran-and-c
import pathlib as p
import shlex
import subprocess
import textwrap
import typing as t

from mpmath import mp, mpf


Path = t.Union[str, p.Path]
mp.dps = 33


class Discrepancy:
    def __init__(self, directory: Path) -> None:
        self.directory = p.Path(directory)
        self.directory.mkdir(parents=True, exist_ok=True)

    def compare(self, clang: str, fortran: str, mpmath: str, **kwargs: str) -> t.Dict[str, mp.mpf]:
        return {
            'clang': mpf(self._clang(clang, **kwargs)),
            'fortran': mpf(self._fortran(fortran, **kwargs)),
            'mpmath': mpf(self._mpmath(mpmath, **kwargs)),
        }

    def _clang(self, expression: str, **kwargs: str) -> None:
        if kwargs:
            assignment = f'double {", ".join(f"{k}={v}" for k, v in kwargs.items())};'
        else:
            assignment = ''
        template = textwrap.dedent(f'''
            #include <stdio.h>
            #include <math.h>

            int main() {{
                {assignment}
                double ans;

                ans = {expression};

                printf("%.{mp.dps}f", ans);

                return 0;
            }}
        ''')
        (self.directory/'code.c').write_text(template)
        self._run('gcc code.c -lm -O3 -o c')
        return self._run('./c').stdout.decode().strip()

    def _fortran(self, expression: str, **kwargs: str) -> str:
        if kwargs:
            assignment = f'real(f64), parameter :: {", ".join(f"{k}={v}_f64" for k, v in kwargs.items())}'
        else:
            assignment = ''
        template = textwrap.dedent(f'''
            program main
                use, intrinsic :: iso_fortran_env, only: f64=>real64
                implicit none

                {assignment}
                real(f64) :: ans

                ans = {expression}

                write(*, "(F99.{mp.dps}))") ans
            end program
        ''')
        (self.directory/'code.f90').write_text(template)
        self._run('gfortran code.f90 -O3 -o fortran')
        return self._run('./fortran').stdout.decode().strip()

    def _mpmath(self, expression: str, **kwargs: str) -> None:
        for key, value in kwargs.items():
            locals()[key] = mpf(value)
        return str(eval(expression))

    def _run(self, command: str) -> subprocess.CompletedProcess:
        args = shlex.split(command)
        return subprocess.run(args, cwd=self.directory, capture_output=True)


if __name__ == '__main__':
    import random

    d = Discrepancy(directory='todo/discrepancy')
    data = {
        'pi': {
            'func': lambda: d.compare('3.14159265358979323846', '4.d0*datan(1.d0)', 'mp.pi'),
            'range': {},
        },
        'e': {
            'func': lambda: d.compare('exp(1.0)', 'dexp(1.d0)', 'mp.e'),
            'range': {},
        },
        'exp': {
            'func': lambda **kwargs: d.compare('exp(a)', 'dexp(a)', 'mp.exp(a)', **kwargs),
            'range': {'a': (-100.0, 100.0)},
        },
        'log': {
            'func': lambda **kwargs: d.compare('log(a)', 'dlog(a)', 'mp.log(a)', **kwargs),
            'range': {'a': (0.01, 100.0)},
        },
        'sin': {
            'func': lambda **kwargs: d.compare('sin(a)', 'dsin(a)', 'mp.sin(a)', **kwargs),
            'range': {'a': (-100.0, 100.0)},
        },
        'cos': {
            'func': lambda **kwargs: d.compare('cos(a)', 'dcos(a)', 'mp.cos(a)', **kwargs),
            'range': {'a': (-100.0, 100.0)},
        },
        'tan': {
            'func': lambda **kwargs: d.compare('tan(a)', 'dtan(a)', 'mp.tan(a)', **kwargs),
            'range': {'a': (-100.0, 100.0)},
        },
        'asin': {
            'func': lambda **kwargs: d.compare('asin(a)', 'dasin(a)', 'mp.asin(a)', **kwargs),
            'range': {'a': (-1.0, 1.0)},
        },
        'acos': {
            'func': lambda **kwargs: d.compare('acos(a)', 'dacos(a)', 'mp.acos(a)', **kwargs),
            'range': {'a': (-1.0, 1.0)},
        },
        'atan': {
            'func': lambda **kwargs: d.compare('atan(a)', 'datan(a)', 'mp.atan(a)', **kwargs),
            'range': {'a': (-100.0, 100.0)},
        },
        'sinh': {
            'func': lambda **kwargs: d.compare('sinh(a)', 'dsinh(a)', 'mp.sinh(a)', **kwargs),
            'range': {'a': (-10.0, 10.0)},
        },
        'cosh': {
            'func': lambda **kwargs: d.compare('cosh(a)', 'dcosh(a)', 'mp.cosh(a)', **kwargs),
            'range': {'a': (-10.0, 10.0)},
        },
        'tanh': {
            'func': lambda **kwargs: d.compare('tanh(a)', 'dtanh(a)', 'mp.tanh(a)', **kwargs),
            'range': {'a': (-100.0, 100.0)},
        },
        'asinh': {
            'func': lambda **kwargs: d.compare('asinh(a)', 'dasinh(a)', 'mp.asinh(a)', **kwargs),
            'range': {'a': (-100.0, 100.0)},
        },
        'acosh': {
            'func': lambda **kwargs: d.compare('acosh(a)', 'dacosh(a)', 'mp.acosh(a)', **kwargs),
            'range': {'a': (1.0, 100.0)},
        },
        'atanh': {
            'func': lambda **kwargs: d.compare('atanh(a)', 'datanh(a)', 'mp.atanh(a)', **kwargs),
            'range': {'a': (-1.0, 1.0)},
        },
        'add': {
            'func': lambda **kwargs: d.compare('a+b', 'a+b', 'a+b', **kwargs),
            'range': {'a': (-100.0, 100.0), 'b': (-100.0, 100.0)},
        },
        'sub': {
            'func': lambda **kwargs: d.compare('a-b', 'a-b', 'a-b', **kwargs),
            'range': {'a': (-100.0, 100.0), 'b': (-100.0, 100.0)},
        },
        'mul': {
            'func': lambda **kwargs: d.compare('a*b', 'a*b', 'a*b', **kwargs),
            'range': {'a': (-100.0, 100.0), 'b': (-100.0, 100.0)},
        },
        'div': {
            'func': lambda **kwargs: d.compare('a/b', 'a/b', 'a/b', **kwargs),
            'range': {'a': (-100.0, 100.0), 'b': (-100.0, 100.0)},
        },
    }
    zero = mpf('0.0')
    for name, group in data.items():
        for _ in range(32):
            kwargs = {
                key: random.random()*(max-min)+min
                for key, (min, max) in group.get('range', {}).items()
            }
            ans = group['func'](**kwargs)
            if ans['clang'] != ans['fortran']:
                print(name, kwargs, ans)
