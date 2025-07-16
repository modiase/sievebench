project('sieve', 'cpp',
  version : '0.1',
  default_options : ['warning_level=3', 'cpp_std=c++17', 'b_lto=true'])

executable('sieve_cpp',
           'sieve.cpp',
           cpp_args : ['-O3', '-march=native'],
           dependencies : [dependency('threads')],
           install : true)
