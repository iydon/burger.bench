use std::f64::consts::PI;

macro_rules! boundary {
    ($u:ident, $N:ident) => {
        $u[3] = $u[$N + 3];
        $u[2] = $u[$N + 2];
        $u[1] = $u[$N + 1];
        $u[0] = $u[$N];
        $u[$N + 4] = $u[4];
        $u[$N + 5] = $u[5];
        $u[$N + 6] = $u[6];
    };
}

fn weno(a: f64, b: f64, c: f64, d: f64, e: f64) -> f64 {
    let beta1 = 13.0/12.0*(a - 2.0*b + c).powi(2) + 1.0/4.0*(a - 4.0*b + 3.0*c).powi(2);
    let beta2 = 13.0/12.0*(b - 2.0*c + d).powi(2) + 1.0/4.0*(b - d).powi(2);
    let beta3 = 13.0/12.0*(c - 2.0*d + e).powi(2) + 1.0/4.0*(3.0*c - 4.0*d + e).powi(2);
    let wf1 = 1.0/10.0 / (beta1 + 1e-6).powi(2);
    let wf2 = 3.0/5.0 / (beta2 + 1e-6).powi(2);
    let wf3 = 3.0/10.0 / (beta3 + 1e-6).powi(2);
    let u1 = 1.0/3.0*a - 7.0/6.0*b + 11.0/6.0*c;
    let u2 = -1.0/6.0*b + 5.0/6.0*c + 1.0/3.0*d;
    let u3 = 1.0/3.0*c + 5.0/6.0*d - 1.0/6.0*e;
    return (wf1*u1 + wf2*u2 + wf3*u3) / (wf1 + wf2 + wf3);
}

fn flux(u: &[f64], jth: usize, dx: f64) -> f64 {
    let upp = weno(u[jth+3], u[jth+2], u[jth+1], u[jth], u[jth-1]);
    let upm = weno(u[jth-2], u[jth-1], u[jth], u[jth+1], u[jth+2]);
    let ump = weno(u[jth+2], u[jth+1], u[jth], u[jth-1], u[jth-2]);
    let umm = weno(u[jth-3], u[jth-2], u[jth-1], u[jth], u[jth+1]);
    let alpha1 = f64::max(upp.abs(), upm.abs());
    let alpha2 = f64::max(ump.abs(), umm.abs());
    let flux1 = 1.0/2.0 * (1.0/2.0*upm.powi(2) + 1.0/2.0*upp.powi(2) - alpha1*(upp-upm)/2.0);
    let flux2 = 1.0/2.0 * (1.0/2.0*umm.powi(2) + 1.0/2.0*ump.powi(2) - alpha2*(ump-umm)/2.0);
    return - (flux1-flux2) / dx;
}

fn diffusion(u: &[f64], jth: usize, dx: f64, re: f64) -> f64 {
    let diffusion_plus = 1.0/12.0*u[jth-1] - 5.0/4.0*u[jth] + 5.0/4.0*u[jth+1] - 1.0/12.0*u[jth+2];
    let diffusion_minus = -11.0/12.0*u[jth-1] + 3.0/4.0*u[jth] + 1.0/4.0*u[jth+1] - 1.0/12.0*u[jth+2];
    return (diffusion_plus-diffusion_minus) / (re*dx.powi(2));
}

fn lu(u: &[f64], jth: usize, dx: f64, re: f64) -> f64 {
    return flux(&u, jth, dx) + diffusion(&u, jth, dx, re);
}

fn main() {
    const RE: f64 = __RE__;
    const N: usize = __N__;
    const L: f64 = __L__;
    const T: f64 = __T__;

    let dx = L / N as f64;
    let dt = __CFL__ * dx;
    let nt = (T / dt) as usize;
    let mut u1 = vec![0.0; N+7];
    let mut u2 = vec![0.0; N+7];
    let mut un = vec![0.0; N+7];
    let mut uold: Vec<f64>;

    for ith in 4..N+4 {
        un[ith] = (
            - (2.0*PI*(ith as f64-2.5)*dx).cos() / (2.0*PI)
            + (2.0*PI*(ith as f64-3.5)*dx).cos() / (2.0*PI)
        ) / dx + 1.0;
    }

    for _ in 0..nt {
        uold = un.clone();
        for jth in 4..N+4 {
            u1[jth] = uold[jth] + dt*lu(&uold, jth, dx, RE);
        }
        boundary!(u1, N);
        for jth in 4..N+4 {
            u2[jth] = 3.0/4.0*uold[jth] + 1.0/4.0*u1[jth] + 1.0/4.0*dt*lu(&u1, jth, dx, RE);
        }
        boundary!(u2, N);
        for jth in 4..N+4 {
            un[jth] = 1.0/3.0*uold[jth] + 2.0/3.0*u2[jth] + 2.0/3.0*dt*lu(&u2, jth, dx, RE);
        }
        boundary!(un, N);
    }

    println!("{:?}", un);
}
