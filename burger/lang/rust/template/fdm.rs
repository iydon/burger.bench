use std::f64::consts::PI;

fn calc(un: &mut Vec<f64>, nt: usize, nx: usize, dt: f64, dx: f64, nu: f64) {
    let mut uold: Vec<f64>;
    for _ in 0..nt {
        uold = un.clone();
        for jth in 1..nx-1 {
            un[jth] = uold[jth]
                - uold[jth]*dt/dx*(uold[jth]-uold[jth-1])
                + nu*dt/dx.powi(2)*(uold[jth+1]-2.0*uold[jth]+uold[jth-1]);
        }
        un[0] = uold[0]
            - uold[0]*dt/dx*(uold[0]-uold[nx-2])
            + nu*dt/dx.powi(2)*(uold[1]-2.0*uold[0]+uold[nx-2]);
        un[nx-1] = un[0];
    }
}

fn main() {
    const RE: f64 = __RE__;
    const N: usize = __N__;
    const L: f64 = __L__;
    const T: f64 = __T__;

    let nu = L / RE;  // u0 = 1
    let dx = L / (N-1) as f64;
    let dt = __CFL__ * dx;
    let nt = (T / dt) as usize;
    let mut un = vec![0.0; N];

    for ith in 0..N {
        un[ith] = (2.0*PI*(ith as f64)*dx/L).sin() + 1.0;
    }

    calc(&mut un, nt, N, dt, dx, nu);

    println!("{:?}", un);
}
