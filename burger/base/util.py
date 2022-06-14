__all__ = ['Proc', 'human']


import io
import os
import pathlib as p
import typing as t


class Proc:
    '''
    - Reference:
        - https://github.com/pixelb/ps_mem
    '''

    PAGESIZE = os.sysconf('SC_PAGE_SIZE') / 1024  # KiB

    fields = {
        'VmPeak', 'VmSize', 'VmLck', 'VmPin', 'VmHWM', 'VmRSS',
        'RssAnon', 'RssFile', 'RssShmem', 'VmData', 'VmStk',
        'VmExe', 'VmLib', 'VmPTE', 'VmSwap', 'HugetlbPages',
    }

    def __init__(self):
        if os.uname()[0] == 'FreeBSD':
            self.proc = p.Path('/compat/linux/proc')
        else:
            self.proc = p.Path('/proc')

    @classmethod
    def new(cls) -> 'Proc':
        return cls()

    def memory(self, pid: int) -> float:
        private, shared, private_huge = 0, 0, 0
        pss_lines = []
        with self._open(pid, 'statm') as f:
            rss = self.PAGESIZE * int(f.readline().split()[1])
        if self._path(pid, 'smaps').exists():
            smaps = 'smaps'
            if self._path(pid, 'smaps_rollup').exists():
                smaps = 'smaps_rollup'
            with self._open(pid, smaps) as f:
                for line in f.readlines():
                    if line.startswith('Private_Hugetlb:'):
                        private_huge += int(line.split()[1])
                    elif line.startswith('Shared'):
                        shared += int(line.split()[1])
                    elif line.startswith('Private'):
                        private += int(line.split()[1])
                    elif line.startswith('Pss:'):
                        pss_lines.append(line)
            if pss_lines:
                adjust = 0.5
                pss = sum(float(line.split()[1])+adjust for line in pss_lines)
                shared = pss - private
            private += private_huge
        else:
            with self.open(pid, 'statm') as f:
                shared = self.PAGESIZE * int(f.readline().split()[2])
            private = rss - shared
        return private + shared

    def status(self, pid: int) -> t.Dict[str, float]:
        '''
        - Reference:
            - https://elinux.org/Runtime_Memory_Measurement
        '''
        assert self._path(pid, 'status').exists()

        result = {}
        with self._open(pid, 'status') as f:
            for line in f.readlines():
                for field in self.fields:
                    if line.startswith(field):
                        result[field] = float(line.split()[1])
        return result

    def _path(self, *args: t.Union[str, int]) -> p.Path:
        return self.proc / p.Path(*map(str, args))

    def _open(self, *args: t.Union[str, int]) -> io.TextIOWrapper:
        return open(self._path(*args), errors='ignore')


def human(num: float, power: str = 'Ki') -> str:
    powers = ['Ki', 'Mi', 'Gi', 'Ti']
    while num >= 1000:
        num /= 1024.0
        power = powers[powers.index(power)+1]
    return f'{num:.2f} {power}B'
