project('sieve_fortran', 'fortran')

executable('sieve_fortran',
           'sieve.f90',
           fortran_args : ['-O3', '-march=native', '-fopenmp'],
           link_args : ['-fopenmp'],
           install : true)
