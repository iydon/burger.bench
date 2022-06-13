program main
    use, intrinsic :: iso_fortran_env, only: f64=>real64
    implicit none

    real(f64), parameter :: PI = 4.d0*datan(1.d0)
    real(f64), parameter :: RE=__RE__, L=__L__, T=__T__
    integer, parameter :: N = __N__

    real(f64) :: dx, dt, lu_value
    real(f64), dimension(N+7) :: u1, u2, un, uold
    integer :: nt, ith, jth

    dx = L / N
    dt = __CFL__ * L / N
    nt = nint(T / dt)
    u1(:) = 0.d0
    u2(:) = 0.d0
    un(:) = 0.d0

    do ith = 5, N+4
        un(ith) = ( &
            - dcos(2.d0*PI*(ith-3.5)*dx) / (2.d0*PI) &
            + dcos(2.d0*PI*(ith-4.5)*dx) / (2.d0*PI) &
        ) / dx + 1.d0
    end do

    do ith = 1, nt
        uold(:) = un(:)
        do jth = 5, N+4
            call lu(uold, N, jth, dx, Re, lu_value)
            u1(jth) = uold(jth) + dt*lu_value
        end do
        call boundary(u1, N)
        do jth = 5, N+4
            call lu(u1, N, jth, dx, Re, lu_value)
            u2(jth) = 3.d0/4.d0*uold(jth) + 1.d0/4.d0*u1(jth) + 1.d0/4.d0*dt*lu_value
        end do
        call boundary(u2, N)
        do jth = 5, N+4
            call lu(u2, N, jth, dx, Re, lu_value)
            un(jth) = 1.d0/3.d0*uold(jth) + 2.d0/3.d0*u2(jth) + 2.d0/3.d0*dt*lu_value
        end do
        call boundary(un, N)
    end do

    write(*, *) un
end program

subroutine boundary(u, N)
    use, intrinsic :: iso_fortran_env, only: f64=>real64
    implicit none

    real(f64), dimension(N+7), intent(inout) :: u
    integer, intent(in) :: N

    u(4) = u(N + 4)
    u(3) = u(N + 3)
    u(2) = u(N + 2)
    u(1) = u(N + 1)
    u(N + 5) = u(5)
    u(N + 6) = u(6)
    u(N + 7) = u(7)
end subroutine

subroutine weno(a, b, c, d, e, result)
    use, intrinsic :: iso_fortran_env, only: f64=>real64
    implicit none

    real(f64), intent(in) :: a, b, c, d, e
    real(f64), intent(out) :: result
    real(f64) :: beta1, beta2, beta3, wf1, wf2, wf3, u1, u2, u3

    beta1 = 13.d0/12.d0*(a - 2.d0*b + c)**2 + 1.d0/4.d0*(a - 4.d0*b + 3.d0*c)**2
    beta2 = 13.d0/12.d0*(b - 2.d0*c + d)**2 + 1.d0/4.d0*(b - d)**2
    beta3 = 13.d0/12.d0*(c - 2.d0*d + e)**2 + 1.d0/4.d0*(3.d0*c - 4.d0*d + e)**2
    wf1 = 1.d0/10.d0 / (beta1 + 1e-6) ** 2
    wf2 = 3.d0/5.d0 / (beta2 + 1e-6) ** 2
    wf3 = 3.d0/10.d0 / (beta3 + 1e-6) ** 2
    u1 = 1.d0/3.d0*a - 7.d0/6.d0*b + 11.d0/6.d0*c
    u2 = -1.d0/6.d0*b + 5.d0/6.d0*c + 1.d0/3.d0*d
    u3 = 1.d0/3.d0*c + 5.d0/6.d0*d - 1.d0/6.d0*e
    result = (wf1*u1 + wf2*u2 + wf3*u3) / (wf1 + wf2 + wf3)
end subroutine

subroutine flux(u, N, jth, dx, result)
    use, intrinsic :: iso_fortran_env, only: f64=>real64
    implicit none

    real(f64), dimension(N+7), intent(inout) :: u
    real(f64), intent(in) :: dx
    integer, intent(in) :: N, jth
    real(f64), intent(out) :: result
    real(f64) :: upp, upm, ump, umm, alpha1, alpha2, flux1, flux2

    call weno(u(jth+3), u(jth+2), u(jth+1), u(jth), u(jth-1), upp)
    call weno(u(jth-2), u(jth-1), u(jth), u(jth+1), u(jth+2), upm)
    call weno(u(jth+2), u(jth+1), u(jth), u(jth-1), u(jth-2), ump)
    call weno(u(jth-3), u(jth-2), u(jth-1), u(jth), u(jth+1), umm)
    alpha1 = max(dabs(upp), dabs(upm))
    alpha2 = max(dabs(ump), dabs(umm))
    flux1 = 1.d0/2.d0 * (1.d0/2.d0*upm**2 + 1.d0/2.d0*upp**2 - alpha1*(upp-upm)/2.d0)
    flux2 = 1.d0/2.d0 * (1.d0/2.d0*umm**2 + 1.d0/2.d0*ump**2 - alpha2*(ump-umm)/2.d0)
    result = - (flux1-flux2) / dx
end subroutine

subroutine diffusion(u, N, jth, dx, Re, result)
    use, intrinsic :: iso_fortran_env, only: f64=>real64
    implicit none

    real(f64), dimension(N+7), intent(inout) :: u
    real(f64), intent(in) :: dx, Re
    integer, intent(in) :: N, jth
    real(f64), intent(out) :: result
    real(f64) :: diffision_plus, diffision_minus

    diffision_plus = 1.d0/12.d0*u(jth-1) - 5.d0/4.d0*u(jth) + 5.d0/4.d0*u(jth+1) - 1.d0/12.d0*u(jth+2)
    diffision_minus = -11.d0/12.d0*u(jth-1) + 3.d0/4.d0*u(jth) + 1.d0/4.d0*u(jth+1) - 1.d0/12.d0*u(jth+2)
    result = (diffision_plus-diffision_minus) / (Re*dx**2)
end subroutine

subroutine lu(u, N, jth, dx, Re, result)
    use, intrinsic :: iso_fortran_env, only: f64=>real64
    implicit none

    real(f64), dimension(N+7), intent(inout) :: u
    real(f64), intent(in) :: dx, Re
    integer, intent(in) :: N, jth
    real(f64), intent(out) :: result
    real(f64) :: flux_value, diffusion_value

    call flux(u, N, jth, dx, flux_value)
    call diffusion(u, N, jth, dx, Re, diffusion_value)
    result = flux_value + diffusion_value
end subroutine
