__all__ = [
    'Expr', 'Function', 'Number', 'Symbol',
    'Registrar', 'Variable',
]


import functools as f
import typing as t

from sympy.core import Expr, Function, Number, Symbol


class Registrar:
    Self = __qualname__

    def __init__(self) -> None:
        self._registry = {}

    def __getitem__(self, key: t.Optional[t.Union[str, t.Callable]] = None) -> t.Callable:
        if isinstance(key, t.Callable):
            return key
        else:
            return self._registry[self._strip(key)]

    @classmethod
    def new(cls) -> Self:
        return cls()

    def register(self, key: t.Optional[str] = None) -> None:
        def decorate(func):
            self._registry[self._strip(key)] = func

            @f.wraps(func)
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)
            return wrapper
        return decorate

    def _strip(self, key: t.Optional[str] = None) -> t.Optional[str]:
        if key is None:
            return
        else:
            return key.strip().lower().replace(' ', '_').replace('-', '_')


class Variable:
    Self = __qualname__
    all = {}

    def __init__(self, name: str) -> None:
        self._name = name
        self._cache = {}

    def __repr__(self) -> str:
        return self._name

    @classmethod
    def from_name(cls, *names: str) -> t.Iterator[Self]:
        for name in names:
            if name not in cls.all:
                cls.all[name] = cls(name)
            yield cls.all[name]

    @property
    def i(self) -> Symbol:
        return self.raw

    @property
    def o(self) -> Symbol:
        return self.zero

    @property
    def d(self) -> Symbol:
        return self.delta

    @property
    def raw(self) -> Symbol:
        return self._sympify(self._name)

    @property
    def zero(self) -> Symbol:
        return self._sympify(f'{self._name}0')

    @property
    def delta(self) -> Symbol:
        return self._sympify(f'Δ{self._name}')

    def _sympy_(self) -> Symbol:
        return self.raw

    def _sympify(self, name: str) -> Symbol:
        if name not in self._cache:
            self._cache[name] = Symbol(name, real=True)
        return self._cache[name]
