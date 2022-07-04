from mpmath import mp, mpf, matrix


# f32: 6, f64: 15, f128: 33, f256: 71
mp.dps = __DPS__
n1, n2, n3, n4, n5, n6, n7, n10, n11, n12, n13, eps = \
    mpf('1.0'), mpf('2.0'), mpf('3.0'), mpf('4.0'), mpf('5.0'), mpf('6.0'), \
    mpf('7.0'), mpf('10.0'), mpf('11.0'), mpf('12.0'), mpf('13.0'), mpf('1e-6')


def calc(un: matrix, nt: int, nx: int, dt: mpf, dx: mpf, nu: mpf) -> matrix:
    for ith in range(nt):
        uold = un.copy()
        for jth in range(1, nx-1):
            un[jth] = uold[jth] \
                - uold[jth]*dt/dx*(uold[jth]-uold[jth-1]) \
                + nu*dt/dx**2*(uold[jth+1]-2*uold[jth]+uold[jth-1])
        un[-1] = un[0] = uold[0] \
            - uold[0]*dt/dx*(uold[0]-uold[-2]) \
            + nu*dt/dx**2*(uold[1]-2*uold[0]+uold[-2])
    return un


if __name__ == '__main__':
    RE = mpf('__RE__')
    L = mpf('__L__')
    T = mpf('__T__')
    N = __N__

    nu = L / RE  # u0=1
    dx = L / N
    dt = mpf('__CFL__') * dx
    nt = int(T / dt)
    un = matrix(N, 1)

    for ith in range(N):
        un[ith] = mp.sin(mpf('2.0')*mp.pi*ith*dx/L) + mpf('1.0')

    un = calc(un, nt, N, dt, dx, nu)

    print(','.join(map(str, un)))
