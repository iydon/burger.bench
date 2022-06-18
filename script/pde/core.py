__all__ = ['PDE1D', 'x', 't', 'u']


import itertools as it
import functools as f
import typing as T

from sympy.core import I
from sympy.functions import exp, factorial
from sympy.ntheory import binomial_coefficients_list
from sympy.printing import pretty
from sympy.series import O

from .macro import __one__, __zero__
from .scheme import registrar, scope
from .type import Expr, Function, Number, Symbol, Variable


x, t = Variable.from_name('x', 't')
u = Function('u')


class PDE1D:
    Self = __qualname__

    def __init__(self, terms: T.List[T.Dict[str, T.Any]]) -> None:
        default = {'scheme': None, 'diff': 0}
        self._terms = [
            {
                'coef': term.get('coef', __one__),
                'func': term.get('func', u(x, t)),
                'part': {
                    x: term.get('part', {}).get(x, default),
                    t: term.get('part', {}).get(t, default),
                }
            } for term in terms
        ]

    def __iter__(self) -> T.Iterator[None]:
        yield from self._terms

    def __getitem__(self, index: int) -> T.Dict[str, T.Any]:
        return self._terms[index]

    def __len__(self) -> int:
        return len(self._terms)

    def __repr__(self) -> str:
        return pretty(self.equation)

    @classmethod
    def from_term(cls, *terms: T.Dict[str, T.Any]) -> Self:
        return cls(terms)

    @f.cached_property
    def equation(self) -> Expr:
        '''PDE'''
        ans = __zero__
        for term in self._terms:
            ans += term['coef'] * term['func'].diff(
                x, term['part'][x]['diff'],
                t, term['part'][t]['diff'],
            )
        return ans.simplify()

    @f.cached_property
    def discrete(self) -> Expr:
        '''离散格式'''
        ans = __zero__
        for term in self._terms:
            coef, func = term['coef'], term['func']
            for key, value in term['part'].items():
                func = registrar[value['scheme']](func, key, value['diff'])
            ans += coef * func
        return ans.simplify().expand()

    @f.cached_property
    def von_neumann(self) -> Expr:
        '''von-Neumann linear stability analysis'''
        sigma, k = Symbol('σ', real=True), Symbol('k', real=True)
        ans = self.discrete
        for nx, nt in it.product(scope, repeat=2):
            ans = ans.subs(
                u(x.o+nx*x.d, t.o+nt*t.d),
                exp(sigma*nt*t.d) * exp(I*k*nx*x.d),
            )
        return ans.expand(complex=True).simplify()

    @f.lru_cache
    def taylor(self, number: int = 3) -> Expr:
        '''离散格式的泰勒展开'''
        ans = self.discrete
        for nx, nt in it.product(scope, repeat=2):
            ans = ans.subs(
                u(x.o+nx*x.d, t.o+nt*t.d),
                self._taylor(u, x, t, nx, nt, number),
            )
        return ans.simplify()

    @f.lru_cache
    def error(self, number: int = 3) -> Expr:
        '''离散格式与 PDE 之间的误差'''
        return (self.equation - self.taylor(number)).simplify()

    def _taylor(
        self,
        func: Function, x: Variable, t: Variable, nx: Number, nt: Number,
        number: int = 3,
    ) -> Expr:
        ans = func(x.i, t.i)
        for ith in range(1, number):
            part = __zero__
            for jth, k in zip(range(ith+1), binomial_coefficients_list(ith)):
                part += k * (nx*x.d)**jth*(nt*t.d)**(ith-jth) \
                          * u(x.i, t.i).diff(x.i, jth, t.i, (ith-jth))
            ans += part / factorial(ith)
        return ans + (O(x.d) + O(t.d))**number
