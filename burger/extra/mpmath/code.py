from mpmath import mp, mpf, matrix


# f32: 6, f64: 15, f128: 33, f256: 71
mp.dps = __DPS__
n1, n2, n3, n4, n5, n6, n7, n10, n11, n12, n13, eps = \
    mpf('1.0'), mpf('2.0'), mpf('3.0'), mpf('4.0'), mpf('5.0'), mpf('6.0'), \
    mpf('7.0'), mpf('10.0'), mpf('11.0'), mpf('12.0'), mpf('13.0'), mpf('1e-6')


def boundary(u: matrix, N: int) -> None:
    u[3] = u[N + 3]
    u[2] = u[N + 2]
    u[1] = u[N + 1]
    u[0] = u[N]
    u[N + 4] = u[4]
    u[N + 5] = u[5]
    u[N + 6] = u[6]

def weno(a: mpf, b: mpf, c: mpf, d: mpf, e: mpf) -> mpf:
    beta1 = n13/n12*(a - n2*b + c)**2 + n1/n4*(a - n4*b + n3*c)**2
    beta2 = n13/n12*(b - n2*c + d)**2 + n1/n4*(b - d)**2
    beta3 = n13/n12*(c - n2*d + e)**2 + n1/n4*(n3*c - n4*d + e)**2
    wf1 = n1/n10 / (beta1 + eps) ** 2
    wf2 = n3/n5 / (beta2 + eps) ** 2
    wf3 = n3/n10 / (beta3 + eps) ** 2
    u1 = n1/n3*a - n7/n6*b + n11/n6*c
    u2 = -n1/n6*b + n5/n6*c + n1/n3*d
    u3 = n1/n3*c + n5/n6*d - n1/n6*e
    return (wf1*u1 + wf2*u2 + wf3*u3) / (wf1 + wf2 + wf3)

def flux(u: matrix, jth: int, dx: mpf) -> mpf:
    upp = weno(u[jth+3], u[jth+2], u[jth+1], u[jth], u[jth-1])
    upm = weno(u[jth-2], u[jth-1], u[jth], u[jth+1], u[jth+2])
    ump = weno(u[jth+2], u[jth+1], u[jth], u[jth-1], u[jth-2])
    umm = weno(u[jth-3], u[jth-2], u[jth-1], u[jth], u[jth+1])
    alpha1 = max(abs(upp), abs(upm))
    alpha2 = max(abs(ump), abs(umm))
    flux1 = n1/n2 * (n1/n2*upm**2 + n1/n2*upp**2 - alpha1*(upp-upm)/n2)
    flux2 = n1/n2 * (n1/n2*umm**2 + n1/n2*ump**2 - alpha2*(ump-umm)/n2)
    return - (flux1-flux2) / dx

def diffusion(u: matrix, jth: int, dx: mpf, RE: mpf) -> mpf:
    diffusion_plus = n1/n12*u[jth-1] - n5/n4*u[jth] + n5/n4*u[jth+1] - n1/n12*u[jth+2]
    diffusion_minus = -n11/n12*u[jth-1] + n3/n4*u[jth] + n1/n4*u[jth+1] - n1/n12*u[jth+2]
    return (diffusion_plus-diffusion_minus) / (RE*dx**2)

def lu(u: matrix, jth: int, dx: mpf, RE: mpf) -> mpf:
    flux_data = flux(u, jth, dx)
    diffusion_data = diffusion(u, jth, dx, RE)
    return flux_data + diffusion_data

def calc(un: matrix, nt: int, N: int, dt: mpf, dx: mpf, RE: mpf) -> matrix:
    u1 = matrix(N+7, 1)
    u2 = matrix(N+7, 1)
    for ith in range(nt):
        uold = un.copy()
        for jth in range(4, N+4):
            lu_value = lu(uold, jth, dx, RE)
            u1[jth] = uold[jth] + dt*lu_value
        boundary(u1, N)
        for jth in range(4, N+4):
            lu_value = lu(u1, jth, dx, RE)
            u2[jth] = n3/n4*uold[jth] + n1/n4*u1[jth] + n1/n4*dt*lu_value
        boundary(u2, N)
        for jth in range(4, N+4):
            lu_value = lu(u2, jth, dx, RE)
            un[jth] = n1/n3*uold[jth] + n2/n3*u2[jth] + n2/n3*dt*lu_value
        boundary(un, N)
    return un


if __name__ == '__main__':
    RE = mpf('__RE__')
    L = mpf('__L__')
    T = mpf('__T__')
    N = __N__

    dx = L / N
    dt = mpf('__CFL__') * dx
    nt = int(T / dt)
    un = matrix(N+7, 1)

    for ith in range(4, N+4):
        un[ith] = (
            - mp.cos(mpf('2.0')*mp.pi*(ith-mpf('2.5'))*dx) / (mpf('2.0')*mp.pi)
            + mp.cos(mpf('2.0')*mp.pi*(ith-mpf('3.5'))*dx) / (mpf('2.0')*mp.pi)
        ) / dx + mpf('1.0')

    un = calc(un, nt, N, dt, dx, RE)

    print(','.join(map(str, un)))
