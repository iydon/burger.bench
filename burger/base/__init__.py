__all__ = ['Bench']


import json
import pathlib as p
import shlex
import subprocess
import tempfile
import time
import typing as t

import numpy as np

from .util import Proc


class Bench:
    '''
    - Reference:
        - https://github.com/greensoftwarelab/Energy-Languages
    '''

    __template__: p.Path

    def __init__(
        self,
        directory: t.Union[str, p.Path] = '.',
        N: int = 1024, RE: float = 200.0, L: float = 1.0, T: float = 2.0,
        CFL: float = 0.1,
    ) -> None:
        self.directory = p.Path(directory)
        self.directory.mkdir(parents=True, exist_ok=True)
        self.parameters = {'N': N, 'RE': RE, 'L': L, 'T': T, 'CFL': CFL}
        self.result = None
        self._is_compiled = False
        self._proc = Proc.new()

    @classmethod
    def version(cls) -> str:
        args = shlex.split(cls._version())
        return subprocess.run(args, capture_output=True).stdout.decode()

    def compile(self) -> 'Bench':
        if not self._is_compiled:
            text = self._render(self.__template__.read_text())
            (self.directory/self.__template__.name).write_text(text)
            for command in self._compile():
                cp = self._raw(command)
                assert cp.returncode==0, cp.stderr.decode()
            self._is_compiled = True
        return self

    def run(self) -> 'Bench':
        self.compile()
        cp = self._raw(self._run())
        assert cp.returncode==0, cp.stderr.decode()
        self.result = np.array(self._parse(cp.stdout.decode()))
        return self

    def reset(self) -> 'Bench':
        self._is_compiled = False
        return self

    def hyperfine(self, warmup: int = 3, min_runs: int = 9) -> t.Dict[str, t.Any]:
        '''
        - Reference:
            - https://github.com/sharkdp/hyperfine
        '''
        self.compile()
        args = ['hyperfine', f"'{self._run()}'"]
        if warmup:
            args += ['--warmup', warmup]
        if min_runs:
            args += ['--min-runs', min_runs]
        with tempfile.NamedTemporaryFile(delete=True) as f:
            args += ['--export-json', f.name]
            cp = self._raw(' '.join(map(str, args)), stdout=True)
            assert cp.returncode == 0
            f.seek(0)
            return json.loads(f.read())['results'][0]

    def memory(self, milliseconds: int = 5) -> t.Dict[str, float]:
        '''
        - Reference:
            - https://github.com/pixelb/ps_mem
        '''
        self.compile()
        min_, max_, total, count = float('inf'), 0.0, 0.0, 0  # KiB
        args = shlex.split(self._run())
        p = subprocess.Popen(args, stdout=subprocess.PIPE, cwd=self.directory)
        while p.poll() is None:
            try:
                memory = self._proc.memory_rss(p.pid)
            except ProcessLookupError:
                break
            min_ = min(min_, memory)
            max_ = max(max_, memory)
            total += memory
            count += 1
            time.sleep(milliseconds/1000)
        return {'min': min_, 'max': max_, 'mean': total/count}

    @classmethod
    def _version(self) -> str:
        raise NotImplementedError

    def _compile(self) -> t.List[str]:
        raise NotImplementedError

    def _run(self) -> str:
        raise NotImplementedError

    def _parse(self, text: str) -> t.List[float]:
        raise NotImplementedError

    def _render(self, text: str) -> str:
        for key, value in self.parameters.items():
            text = text.replace(f'__{key}__', str(value))
        return text

    def _raw(self, command: str, stdout: bool = False) -> subprocess.CompletedProcess:
        args = shlex.split(command)
        return subprocess.run(args, cwd=self.directory, capture_output=not stdout)
