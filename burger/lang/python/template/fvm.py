import numpy as np

from numba import njit


@njit(inline='always')
def boundary(u: np.ndarray, N: int) -> None:
    u[3] = u[N + 3]
    u[2] = u[N + 2]
    u[1] = u[N + 1]
    u[0] = u[N]
    u[N + 4] = u[4]
    u[N + 5] = u[5]
    u[N + 6] = u[6]

@njit
def weno(a: float, b: float, c: float, d: float, e: float) -> float:
    beta1 = 13.0/12.0*(a - 2.0*b + c)**2 + 1.0/4.0*(a - 4.0*b + 3.0*c)**2
    beta2 = 13.0/12.0*(b - 2.0*c + d)**2 + 1.0/4.0*(b - d)**2
    beta3 = 13.0/12.0*(c - 2.0*d + e)**2 + 1.0/4.0*(3.0*c - 4.0*d + e)**2
    wf1 = 1.0/10.0 / (beta1 + 1e-6) ** 2
    wf2 = 3.0/5.0 / (beta2 + 1e-6) ** 2
    wf3 = 3.0/10.0 / (beta3 + 1e-6) ** 2
    u1 = 1.0/3.0*a - 7.0/6.0*b + 11.0/6.0*c
    u2 = -1.0/6.0*b + 5.0/6.0*c + 1.0/3.0*d
    u3 = 1.0/3.0*c + 5.0/6.0*d - 1.0/6.0*e
    return (wf1*u1 + wf2*u2 + wf3*u3) / (wf1 + wf2 + wf3)

@njit
def flux(u: np.ndarray, jth: int, dx: float) -> float:
    upp = weno(u[jth+3], u[jth+2], u[jth+1], u[jth], u[jth-1])
    upm = weno(u[jth-2], u[jth-1], u[jth], u[jth+1], u[jth+2])
    ump = weno(u[jth+2], u[jth+1], u[jth], u[jth-1], u[jth-2])
    umm = weno(u[jth-3], u[jth-2], u[jth-1], u[jth], u[jth+1])
    alpha1 = max(abs(upp), abs(upm))
    alpha2 = max(abs(ump), abs(umm))
    flux1 = 1.0/2.0 * (1.0/2.0*upm**2 + 1.0/2.0*upp**2 - alpha1*(upp-upm)/2.0)
    flux2 = 1.0/2.0 * (1.0/2.0*umm**2 + 1.0/2.0*ump**2 - alpha2*(ump-umm)/2.0)
    return - (flux1-flux2) / dx

@njit
def diffusion(u: np.ndarray, jth: int, dx: float, RE: float) -> float:
    diffusion_plus = 1.0/12.0*u[jth-1] - 5.0/4.0*u[jth] + 5.0/4.0*u[jth+1] - 1.0/12.0*u[jth+2]
    diffusion_minus = -11.0/12.0*u[jth-1] + 3.0/4.0*u[jth] + 1.0/4.0*u[jth+1] - 1.0/12.0*u[jth+2]
    return (diffusion_plus-diffusion_minus) / (RE*dx**2)

@njit
def lu(u: np.ndarray, jth: int, dx: float, RE: float) -> float:
    flux_data = flux(u, jth, dx)
    diffusion_data = diffusion(u, jth, dx, RE)
    return flux_data + diffusion_data

@njit
def calc(un: np.ndarray, nt: int, N: int, dt: float, dx: float, RE: float) -> np.ndarray:
    u1 = np.zeros(N+7)
    u2 = np.zeros(N+7)
    for _ in range(nt):
        uold = un.copy()
        for jth in range(4, N+4):
            lu_value = lu(uold, jth, dx, RE)
            u1[jth] = uold[jth] + dt*lu_value
        boundary(u1, N)
        for jth in range(4, N+4):
            lu_value = lu(u1, jth, dx, RE)
            u2[jth] = 3.0/4.0*uold[jth] + 1.0/4.0*u1[jth] + 1.0/4.0*dt*lu_value
        boundary(u2, N)
        for jth in range(4, N+4):
            lu_value = lu(u2, jth, dx, RE)
            un[jth] = 1.0/3.0*uold[jth] + 2.0/3.0*u2[jth] + 2.0/3.0*dt*lu_value
        boundary(un, N)
    return un


if __name__ == '__main__':
    RE = __RE__
    N = __N__
    L = __L__
    T = __T__

    dx = L / N
    dt = __CFL__ * dx
    nt = int(T / dt)
    un = np.zeros(N+7)

    for ith in range(4, N+4):
        un[ith] = (
            - np.cos(2.0*np.pi*(ith-2.5)*dx) / (2.0*np.pi)
            + np.cos(2.0*np.pi*(ith-3.5)*dx) / (2.0*np.pi)
        ) / dx + 1.0

    un = calc(un, nt, N, dt, dx, RE)

    print(','.join(map(str, un)))
