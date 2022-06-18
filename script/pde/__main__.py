from sympy.core import Symbol
from sympy.printing import pretty_print

from pde import PDE1D, x, t, u
from pde.macro import __one__


nu = Symbol('nu', real=True)

pde = PDE1D.from_term(
    {
        'coef': __one__,
        'func': u(x, t),
        'part': {
            x: {'scheme': None, 'diff': 0},
            t: {'scheme': 'Forward', 'diff': 1},
        },
    }, {
        'coef': __one__ / 2,
        'func': u(x, t)**2,
        'part': {
            x: {'scheme': 'Central', 'diff': 1},
            t: {'scheme': 'Adams-Bashforth', 'diff': 0},
        },
    }, {
        'coef': -nu,
        'func': u(x, t),
        'part': {
            x: {'scheme': 'Central', 'diff': 2},
            t: {'scheme': 'Crank-Nicolson', 'diff': 0},
        },
    },
)

pretty_print(pde.equation)
pretty_print(pde.discrete)
pretty_print(pde.taylor(2))
pretty_print(pde.error(2))
pretty_print(pde.von_neumann)
