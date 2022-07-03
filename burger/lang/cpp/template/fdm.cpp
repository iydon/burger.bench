#include <cmath>
#include <iostream>

#define PI 3.14159265358979323846
#define pow2(x) ((x)*(x))

#define N __N__
#define RE __RE__
#define L __L__
#define T __T__

void calc(double *un, size_t nt, size_t nx, double dt, double dx, double nu) {
    double *uold = new double [nx];
    size_t ith, jth;

    for (ith=0; ith<nt; ith++) {
        for (jth=0; jth<nx; jth++) {
            uold[jth] = un[jth];
        }
        for (jth=1; jth<nx-1; jth++) {
            un[jth] = uold[jth]
                - uold[jth]*dt/dx*(uold[jth]-uold[jth-1])
                + nu*dt/pow2(dx)*(uold[jth+1]-2.0*uold[jth]+uold[jth-1]);
        }
        un[0] = uold[0]
            - uold[0]*dt/dx*(uold[0]-uold[nx-2])
            + nu*dt/pow2(dx)*(uold[1]-2.0*uold[0]+uold[nx-2]);
        un[nx-1] = un[0];
    }

    delete [] uold;
}

void print_array(double *array, size_t length) {
    std::cout.precision(17);
    for (size_t ith=0; ith<length; ith++) {
        std::cout << array[ith] << ", ";
    }
    std::cout << std::endl;
}

int main() {
    double nu = L / RE;  // u0 = 1
    double dx = L / (double) (N-1);
    double dt = __CFL__ * dx;
    double nt = (size_t) (T / dt);
    double *un = new double [N];

    size_t ith;

    for (ith=0; ith<N; ith++) {
        un[ith] = sin(2.0*PI*(double) ith*dx/L) + 1.0;
    }

    calc(un, nt, N, dt, dx, nu);

    print_array(un, N);

    delete [] un;

    return 0;
}
