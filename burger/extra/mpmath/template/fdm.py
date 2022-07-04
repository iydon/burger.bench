from mpmath import mp, mpf, matrix


# f32: 6, f64: 15, f128: 33, f256: 71
mp.dps = __DPS__
n2 = mpf('2.0')


def calc(un: matrix, nt: int, nx: int, dt: mpf, dx: mpf, nu: mpf) -> None:
    for _ in range(nt):
        uold = un.copy()
        for jth in range(1, nx-1):
            un[jth] = uold[jth] \
                - uold[jth]*dt/dx*(uold[jth]-uold[jth-1]) \
                + nu*dt/dx**2*(uold[jth+1]-n2*uold[jth]+uold[jth-1])
        un[nx-1] = un[0] = uold[0] \
            - uold[0]*dt/dx*(uold[0]-uold[nx-2]) \
            + nu*dt/dx**2*(uold[1]-n2*uold[0]+uold[nx-2])


if __name__ == '__main__':
    RE = mpf('__RE__')
    L = mpf('__L__')
    T = mpf('__T__')
    N = __N__

    nu = L / RE  # u0=1
    dx = L / (N-1)
    dt = mpf('__CFL__') * dx
    nt = int(T / dt)

    un = mp.matrix(N, 1)
    for ith, x in enumerate(mp.linspace(mpf('0.0'), L, N)):
        un[ith] = mp.sin(mpf('2.0')*mp.pi*x/L) + mpf('1.0')

    calc(un, nt, N, dt, dx, nu)

    print(','.join(map(str, un)))
