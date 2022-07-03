@inbounds \
function calc(un::Matrix{Float64}, nt::Int, nx::Int, dt::Float64, dx::Float64, nu::Float64)
    for ith = 0: nt-1
        uold = copy(un);
        for jth = 1: nx-2
            un[jth+1] = uold[jth+1] +
                - uold[jth+1]*dt/dx*(uold[jth+1]-uold[jth]) +
                + nu*dt/dx^2*(uold[jth+2]-2.0*uold[jth+1]+uold[jth]);
        end
        un[1] = uold[1] +
            - uold[1]*dt/dx*(uold[1]-uold[nx-1]) +
            + nu*dt/dx^2*(uold[2]-2.0*uold[1]+uold[nx-1]);
        un[nx] = un[1];
    end
end

const RE = __RE__;
const N = __N__;
const L = __L__;
const T = __T__;

const nu = L / RE;  # u0 = 1
const dx = L / (N-1);
const dt = __CFL__ * dx;
const nt = floor(Int, T / dt);
global un = zeros(1, N);

for ith = 0: N-1
    un[ith+1] = sin(2.0*pi*ith*dx/L) + 1.0;
end

calc(un, nt, N, dt, dx, nu);

println(un);
