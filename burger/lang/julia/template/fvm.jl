@inbounds \
function boundary(u::Matrix{Float64}, N::Int)
    u[4] = u[N + 4];
    u[3] = u[N + 3];
    u[2] = u[N + 2];
    u[1] = u[N + 1];
    u[N + 5] = u[5];
    u[N + 6] = u[6];
    u[N + 7] = u[7];
end

function weno(a::Float64, b::Float64, c::Float64, d::Float64, e::Float64)::Float64
    beta1 = 13.0/12.0*(a - 2.0*b + c)^2 + 1.0/4.0*(a - 4.0*b + 3.0*c)^2;
    beta2 = 13.0/12.0*(b - 2.0*c + d)^2 + 1.0/4.0*(b - d)^2;
    beta3 = 13.0/12.0*(c - 2.0*d + e)^2 + 1.0/4.0*(3.0*c - 4.0*d + e)^2;
    wf1 = 1.0/10.0 / (beta1 + 1e-6) ^ 2;
    wf2 = 3.0/5.0 / (beta2 + 1e-6) ^ 2;
    wf3 = 3.0/10.0 / (beta3 + 1e-6) ^ 2;
    u1 = 1.0/3.0*a - 7.0/6.0*b + 11.0/6.0*c;
    u2 = -1.0/6.0*b + 5.0/6.0*c + 1.0/3.0*d;
    u3 = 1.0/3.0*c + 5.0/6.0*d - 1.0/6.0*e;
    return (wf1*u1 + wf2*u2 + wf3*u3) / (wf1 + wf2 + wf3);
end

@inbounds \
function flux(u::Matrix{Float64}, jth::Int, dx::Float64)::Float64
    upp = weno(u[jth+4], u[jth+3], u[jth+2], u[jth+1], u[jth]);
    upm = weno(u[jth-1], u[jth], u[jth+1], u[jth+2], u[jth+3]);
    ump = weno(u[jth+3], u[jth+2], u[jth+1], u[jth], u[jth-1]);
    umm = weno(u[jth-2], u[jth-1], u[jth], u[jth+1], u[jth+2]);
    alpha1 = max(abs(upp), abs(upm));
    alpha2 = max(abs(ump), abs(umm));
    flux1 = 1.0/2.0 * (1.0/2.0*upm^2 + 1.0/2.0*upp^2 - alpha1*(upp-upm)/2.0);
    flux2 = 1.0/2.0 * (1.0/2.0*umm^2 + 1.0/2.0*ump^2 - alpha2*(ump-umm)/2.0);
    return - (flux1-flux2) / dx;
end

@inbounds \
function diffusion(u::Matrix{Float64}, jth::Int, dx::Float64, Re::Float64)::Float64
    diffusion_plus = 1.0/12.0*u[jth] - 5.0/4.0*u[jth+1] + 5.0/4.0*u[jth+2] - 1.0/12.0*u[jth+3];
    diffusion_minus = -11.0/12.0*u[jth] + 3.0/4.0*u[jth+1] + 1.0/4.0*u[jth+2] - 1.0/12.0*u[jth+3];
    return (diffusion_plus-diffusion_minus) / (Re*dx^2);
end

function lu(u::Matrix{Float64}, jth::Int, dx::Float64, Re::Float64)::Float64
    return flux(u, jth, dx) + diffusion(u, jth, dx, Re);
end


const Re = __RE__;
const N = __N__;
const L = __L__;
const T = __T__;

const dx = L / N;
const dt = __CFL__ * dx;
const nt = floor(T / dt);
global u1 = zeros(1, N+7);
global u2 = zeros(1, N+7);
global un = zeros(1, N+7);

for ith = 4: N+3
    un[ith+1] = (
        - cos(2.0*pi*(ith-2.5)*dx) / (2.0*pi)
        + cos(2.0*pi*(ith-3.5)*dx) / (2.0*pi)
    ) / dx + 1.0;
end

@inbounds \
for ith = 1: nt
    uold = copy(un);
    for jth = 4: N+3
        u1[jth+1] = uold[jth+1] + dt*lu(uold, jth, dx, Re);
    end
    boundary(u1, N);
    for jth = 4: N+3
        u2[jth+1] = 3.0/4.0*uold[jth+1] + 1.0/4.0*u1[jth+1] + 1.0/4.0*dt*lu(u1, jth, dx, Re);
    end
    boundary(u2, N);
    for jth = 4: N+3
        un[jth+1] = 1.0/3.0*uold[jth+1] + 2.0/3.0*u2[jth+1] + 2.0/3.0*dt*lu(u2, jth, dx, Re);
    end
    boundary(un, N);
end

println(un);
