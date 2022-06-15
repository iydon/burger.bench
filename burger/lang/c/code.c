#include <stdlib.h>
#include <stdio.h>
#include <math.h>

#define PI 3.14159265358979323846
#define pow2(x) ((x)*(x))
#define max(a,b) ((a)>(b)?(a):(b))

#define N __N__
#define RE __RE__
#define L __L__
#define T __T__

void boundary(double *u) {
        u[3] = u[N + 3];
        u[2] = u[N + 2];
        u[1] = u[N + 1];
        u[0] = u[N];
        u[N + 4] = u[4];
        u[N + 5] = u[5];
        u[N + 6] = u[6];
}

double weno(double a, double b, double c, double d, double e) {
    double beta1 = 13.0/12.0*pow2(a - 2.0*b + c) + 1.0/4.0*pow2(a - 4.0*b + 3.0*c);
    double beta2 = 13.0/12.0*pow2(b - 2.0*c + d) + 1.0/4.0*pow2(b - d);
    double beta3 = 13.0/12.0*pow2(c - 2.0*d + e) + 1.0/4.0*pow2(3.0*c - 4.0*d + e);
    double wf1 = 1.0/10.0 / pow2(beta1 + 1e-6);
    double wf2 = 3.0/5.0 / pow2(beta2 + 1e-6);
    double wf3 = 3.0/10.0 / pow2(beta3 + 1e-6);
    double u1 = 1.0/3.0*a - 7.0/6.0*b + 11.0/6.0*c;
    double u2 = -1.0/6.0*b + 5.0/6.0*c + 1.0/3.0*d;
    double u3 = 1.0/3.0*c + 5.0/6.0*d - 1.0/6.0*e;
    return (wf1*u1 + wf2*u2 + wf3*u3) / (wf1 + wf2 + wf3);
}

double flux(double *u, size_t jth, double dx) {
    double upp = weno(u[jth+3], u[jth+2], u[jth+1], u[jth], u[jth-1]);
    double upm = weno(u[jth-2], u[jth-1], u[jth], u[jth+1], u[jth+2]);
    double ump = weno(u[jth+2], u[jth+1], u[jth], u[jth-1], u[jth-2]);
    double umm = weno(u[jth-3], u[jth-2], u[jth-1], u[jth], u[jth+1]);
    double alpha1 = max(fabs(upp), fabs(upm));
    double alpha2 = max(fabs(ump), fabs(umm));
    double flux1 = 1.0/2.0 * (1.0/2.0*pow2(upm) + 1.0/2.0*pow2(upp) - alpha1*(upp-upm)/2.0);
    double flux2 = 1.0/2.0 * (1.0/2.0*pow2(umm) + 1.0/2.0*pow2(ump) - alpha2*(ump-umm)/2.0);
    return - (flux1-flux2) / dx;
}

double diffusion(double *u, size_t jth, double dx) {
    double diffusion_plus = 1.0/12.0*u[jth-1] - 5.0/4.0*u[jth] + 5.0/4.0*u[jth+1] - 1.0/12.0*u[jth+2];
    double diffusion_minus = -11.0/12.0*u[jth-1] + 3.0/4.0*u[jth] + 1.0/4.0*u[jth+1] - 1.0/12.0*u[jth+2];
    return (diffusion_plus-diffusion_minus) / (RE*pow2(dx));
}

double lu(double *u, size_t jth, double dx) {
    return flux(u, jth, dx) + diffusion(u, jth, dx);
}

void print_array(double *array, size_t length) {
    for (size_t ith=0; ith<length; ith++) {
        printf("%.17f, ", array[ith]);
    }
    printf("\n");
}

int main() {
    double dx = L / (double) N;
    double dt = __CFL__ * dx;
    size_t nt = (size_t) (T / dt);
    double *u1, *u2, *un, *uold;
    u1 = (double*) calloc((N+7), sizeof(double));
    u2 = (double*) calloc((N+7), sizeof(double));
    un = (double*) calloc((N+7), sizeof(double));
    uold = (double*) calloc((N+7), sizeof(double));

    size_t ith, jth;

    for (ith=4; ith<N+4; ith++) {
        un[ith] = (
            - cos(2.0*PI*((double) ith - 2.5)*dx) / (2.0*PI)
            + cos(2.0*PI*((double) ith - 3.5)*dx) / (2.0*PI)
        ) / dx + 1.0;
    }

    for (ith=0; ith<nt; ith++) {
        for (jth=0; jth<N+7; jth++) {
            uold[jth] = un[jth];
        }
        for (jth=4; jth<N+4; jth++) {
            u1[jth] = uold[jth] + dt*lu(uold, jth, dx);
        }
        boundary(u1);
        for (jth=4; jth<N+4; jth++) {
            u2[jth] = 3.0/4.0*uold[jth] + 1.0/4.0*u1[jth] + 1.0/4.0*dt*lu(u1, jth, dx);
        }
        boundary(u2);
        for (jth=4; jth<N+4; jth++) {
            un[jth] = 1.0/3.0*uold[jth] + 2.0/3.0*u2[jth] + 2.0/3.0*dt*lu(u2, jth, dx);
        }
        boundary(un);
    }

    print_array(un, N+7);

    free(u1);
    u1 = NULL;
    free(u2);
    u2 = NULL;
    free(un);
    un = NULL;
    free(uold);
    uold = NULL;

    return 0;
}
