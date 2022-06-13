package main

import (
    "fmt"
    "math"
)

func main() {
    const RE float64 = __RE__;
    const N uint = __N__;
    const L float64 = __L__;
    const T float64 = __T__;

    dx := L / float64(N);
    dt := __CFL__ * dx;
    nt := uint(T / dt);
    u1 := make([]float64, N+7);
    u2 := make([]float64, N+7);
    un := make([]float64, N+7);

    var ith, jth uint;

    for ith=4; ith<N+4; ith++ {
        un[ith] = (-math.Cos(2.0*math.Pi*(float64(ith)-2.5)*dx) / (2.0*math.Pi) + math.Cos(2.0*math.Pi*(float64(ith)-3.5)*dx) / (2.0*math.Pi)) / dx + 1.0;
    }

    for ith=0; ith<nt; ith++ {
        uold := un;
        for jth=4; jth<N+4; jth++ {
            u1[jth] = uold[jth] + dt*lu(uold, jth, dx, RE);
        }
        boundary(u1, N);
        for jth=4; jth<N+4; jth++ {
            u2[jth] = 3.0/4.0*uold[jth] + 1.0/4.0*u1[jth] + 1.0/4.0*dt*lu(u1, jth, dx, RE);
        }
        boundary(u2, N);
        for jth=4; jth<N+4; jth++ {
            un[jth] = 1.0/3.0*uold[jth] + 2.0/3.0*u2[jth] + 2.0/3.0*dt*lu(u2, jth, dx, RE);
        }
        boundary(un, N);
    }

    fmt.Println(un);
}

func boundary(u []float64, N uint) {
    u[3] = u[N + 3];
    u[2] = u[N + 2];
    u[1] = u[N + 1];
    u[0] = u[N];
    u[N + 4] = u[4];
    u[N + 5] = u[5];
    u[N + 6] = u[6];
}

func weno(a float64, b float64, c float64, d float64, e float64) float64 {
    beta1 := 13.0/12.0*math.Pow(a - 2.0*b + c, 2) + 1.0/4.0*math.Pow(a - 4.0*b + 3.0*c, 2);
    beta2 := 13.0/12.0*math.Pow(b - 2.0*c + d, 2) + 1.0/4.0*math.Pow(b - d, 2);
    beta3 := 13.0/12.0*math.Pow(c - 2.0*d + e, 2) + 1.0/4.0*math.Pow(3.0*c - 4.0*d + e, 2);
    wf1 := 1.0/10.0 / math.Pow(beta1 + 1e-6, 2);
    wf2 := 3.0/5.0 / math.Pow(beta2 + 1e-6, 2);
    wf3 := 3.0/10.0 / math.Pow(beta3 + 1e-6, 2);
    u1 := 1.0/3.0*a - 7.0/6.0*b + 11.0/6.0*c;
    u2 := -1.0/6.0*b + 5.0/6.0*c + 1.0/3.0*d;
    u3 := 1.0/3.0*c + 5.0/6.0*d - 1.0/6.0*e;
    return (wf1*u1 + wf2*u2 + wf3*u3) / (wf1 + wf2 + wf3);
}

func flux(u []float64, jth uint, dx float64) float64 {
    upp := weno(u[jth+3], u[jth+2], u[jth+1], u[jth], u[jth-1]);
    upm := weno(u[jth-2], u[jth-1], u[jth], u[jth+1], u[jth+2]);
    ump := weno(u[jth+2], u[jth+1], u[jth], u[jth-1], u[jth-2]);
    umm := weno(u[jth-3], u[jth-2], u[jth-1], u[jth], u[jth+1]);
    alpha1 := math.Max(math.Abs(upp), math.Abs(upm));
    alpha2 := math.Max(math.Abs(ump), math.Abs(umm));
    flux1 := 1.0/2.0 * (1.0/2.0*math.Pow(upm, 2) + 1.0/2.0*math.Pow(upp, 2) - alpha1*(upp-upm)/2.0);
    flux2 := 1.0/2.0 * (1.0/2.0*math.Pow(umm, 2) + 1.0/2.0*math.Pow(ump, 2) - alpha2*(ump-umm)/2.0);
    return - (flux1-flux2) / dx;
}

func diffusion(u []float64, jth uint, dx float64, re float64) float64 {
    diffision_plus := 1.0/12.0*u[jth-1] - 5.0/4.0*u[jth] + 5.0/4.0*u[jth+1] - 1.0/12.0*u[jth+2];
    diffision_minus := -11.0/12.0*u[jth-1] + 3.0/4.0*u[jth] + 1.0/4.0*u[jth+1] - 1.0/12.0*u[jth+2];
    return (diffision_plus-diffision_minus) / (re*math.Pow(dx, 2));
}

func lu(u []float64, jth uint, dx float64, re float64) float64 {
    return flux(u, jth, dx) + diffusion(u, jth, dx, re);
}
