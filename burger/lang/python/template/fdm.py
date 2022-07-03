import numpy as np

from numba import njit


def calc(un: np.ndarray, nt: int, N: int, dt: float, dx: float, nu: float) -> np.ndarray:
    for _ in range(nt):
        uold = un.copy()
        for jth in range(1, N-1):
            un[jth] = uold[jth] \
                - uold[jth]*dt/dx*(uold[jth]-uold[jth-1]) \
                + nu*dt/dx**2*(uold[jth+1]-2*uold[jth]+uold[jth-1])
        un[-1] = un[0] = uold[0] \
            - uold[0]*dt/dx*(uold[0]-uold[-2]) \
            + nu*dt/dx**2*(uold[1]-2*uold[0]+uold[-2])
    return un


if __name__ == '__main__':
    RE = __RE__
    N = __N__
    L = __L__
    T = __T__

    nu = L / RE  # u=1
    dx = L / (N-1)
    dt = __CFL__ * dx
    nt = int(T / dt)
    xs = np.linspace(0.0, L, N)
    un = np.sin(2*np.pi*xs/L) + 1

    un = calc(un, nt, N, dt, dx, nu)

    print(','.join(map(str, un)))
