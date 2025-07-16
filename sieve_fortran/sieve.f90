program sieve_fortran
  use omp_lib
  implicit none

  integer(kind=8) :: n
  character(len=32) :: arg
  integer :: status
  logical, allocatable :: is_prime(:)
  integer(kind=8) :: p, i, limit, count

  ! Get P from the command line and calculate N = 10^P
  if (command_argument_count() /= 1) then
    write(*, '(a)') "Usage: ./sieve_fortran <P>"
    write(*, '(a)') "Calculates primes up to 10^P"
    stop 1
  end if
  call get_command_argument(1, arg, status=status)
  read(arg, *) p
  n = 10**p

  if (n < 2) then
    count = 0
  else
    limit = int(sqrt(real(n, kind=8)))
    allocate(is_prime(0:n))
    is_prime = .true.
    is_prime(0:1) = .false.

    !$omp parallel do schedule(dynamic)
    do p = 2, limit
      if (is_prime(p)) then
        do i = p * p, n, p
          is_prime(i) = .false.
        end do
      end if
    end do
    !$omp end parallel do

    count = 0
    do i = 2, n
      if (is_prime(i)) then
        count = count + 1
      end if
    end do
    deallocate(is_prime)
  end if

  write(*, '("Found ", i0, " primes smaller than ", i0, ".")') count, n

end program sieve_fortran
