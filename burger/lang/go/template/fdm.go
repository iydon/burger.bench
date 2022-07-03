package main

import (
    "fmt"
    "math"
)

func main() {
    const RE float64 = __RE__
    const N uint = __N__
    const L float64 = __L__
    const T float64 = __T__

    nu := L / RE  // u0 = 1
    dx := L / float64(N)
    dt := __CFL__ * dx
    nt := uint(T / dt)
    un := make([]float64, N)

    var ith uint

    for ith=0; ith<N; ith++ {
        un[ith] = math.Sin(2.0*math.Pi*float64(ith)*dx/L) + 1.0
    }

    calc(un, nt, N, dt, dx, nu)

    fmt.Println(un)
}

func pow2(x float64) float64 {
    return x * x
}

func calc(un []float64, nt uint, nx uint, dt float64, dx float64, nu float64) {
    var ith, jth uint
    uold := make([]float64, nx)
    for ith=0; ith<nt; ith++ {
        copy(uold, un)
        for jth=1; jth<nx-1; jth++ {
            un[jth] = uold[jth] - uold[jth]*dt/dx*(uold[jth]-uold[jth-1]) + nu*dt/pow2(dx)*(uold[jth+1]-2.0*uold[jth]+uold[jth-1])
        }
        un[0] = uold[0] - uold[0]*dt/dx*(uold[0]-uold[nx-2]) + nu*dt/pow2(dx)*(uold[1]-2.0*uold[0]+uold[nx-2])
        un[nx-1] = un[0]
    }
}
