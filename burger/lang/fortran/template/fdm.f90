program main
    use, intrinsic :: iso_fortran_env, only: f64=>real64
    implicit none

    real(f64), parameter :: PI = 4.d0*datan(1.d0)
    real(f64), parameter :: RE=__RE__, L=__L__, T=__T__
    integer, parameter :: N = __N__

    real(f64) :: nu, dx, dt
    real(f64), dimension(:), allocatable :: un
    integer :: nt, ith

    allocate(un(N))

    nu = L / RE  ! u0 = 1
    dx = L / (N-1)
    dt = __CFL__ * dx
    nt = idnint(T / dt)
    un(:) = 0.d0

    do ith = 0, N-1
        un(ith+1) = dsin(2.d0*PI*dble(ith)*dx/L) + 1.d0
    end do

    call calc(un, nt, N, dt, dx, nu)

    write(*, *) un

    deallocate(un)
end program

subroutine calc(un, nt, nx, dt, dx, nu)
    use, intrinsic :: iso_fortran_env, only: f64=>real64
    implicit none

    real(f64), dimension(nx), intent(inout) :: un
    real(f64), intent(in) :: dt, dx, nu
    integer, intent(in) :: nt, nx

    real(f64), dimension(:), allocatable :: uold
    integer :: ith, jth

    allocate(uold(nx))

    do ith = 0, nt-1
        uold(:) = un(:)
        do jth = 1, nx-2
            un(jth+1) = ( &
                + uold(jth+1) &
                - uold(jth+1)*dt/dx*(uold(jth+1)-uold(jth)) &
                + nu*dt/dx**2*(uold(jth+2)-2.d0*uold(jth+1)+uold(jth)) &
            )
        end do
        un(1) = ( &
            + uold(1) &
            - uold(1)*dt/dx*(uold(1)-uold(nx-1)) &
            + nu*dt/dx**2*(uold(2)-2.d0*uold(1)+uold(nx-1)) &
        )
        un(nx) = un(1)
    end do

    deallocate(uold)
end subroutine
