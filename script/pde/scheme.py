__all__ = ['registrar', 'scope']


from .type import Expr, Registrar, Variable


registrar = Registrar.new()
scope = {-1, 0, 1}


@registrar.register(None)
def default(func: Expr, v: Variable, order: int) -> Expr:
    g = lambda nv: func.subs(v.i, v.o+nv*v.d)
    if order == 0:
        return g(0)
    else:
        raise NotImplementedError

@registrar.register('Forward')
def _(func: Expr, v: Variable, order: int) -> Expr:
    g = lambda nv: func.subs(v.i, v.o+nv*v.d)
    if order == 1:
        return (g(1) - g(0)) / v.d
    else:
        raise NotImplementedError

@registrar.register('Backward')
def _(func: Expr, v: Variable, order: int) -> Expr:
    g = lambda nv: func.subs(v.i, v.o+nv*v.d)
    if order == 1:
        return (g(0) - g(-1)) / v.d
    else:
        raise NotImplementedError

@registrar.register('Central')
def _(func: Expr, v: Variable, order: int) -> Expr:
    g = lambda nv: func.subs(v.i, v.o+nv*v.d)
    if order == 1:
        return (g(1) - g(-1)) / (2*v.d)
    elif order == 2:
        return (g(1) - 2*g(0) + g(-1)) / v.d**2
    else:
        raise NotImplementedError

@registrar.register('Adams-Bashforth')
def _(func: Expr, v: Variable, order: int) -> Expr:
    g = lambda nv: func.subs(v.i, v.o+nv*v.d)
    return (3*g(0) - g(-1)) / 2

@registrar.register('Crank-Nicolson')
def _(func: Expr, v: Variable, order: int) -> Expr:
    g = lambda nv: func.subs(v.i, v.o+nv*v.d)
    return (g(0) + g(1)) / 2
