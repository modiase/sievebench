# Multi-Language Sieve of Eratosthenes Benchmark

This project implements a parallelized Sieve of Eratosthenes algorithm in Go, C++, and Rust to find all prime numbers up to a given integer N. It includes a Python script to benchmark the performance of each implementation.

## Prerequisites

This project uses the [Nix package manager](https://nixos.org/) to provide a consistent development environment with all the necessary compilers and build tools.

To enter the development environment, run:
```sh
nix develop
```
All subsequent commands should be run from within this shell.

## Building and Running Manually

You can build and run each language's implementation individually. Replace `10000000` with the desired upper limit (N).

### Go

```sh
cd sieve_go
go run . 10000000
```

To build an optimized executable:
```sh
cd sieve_go
go build -ldflags="-s -w" -o sieve_go .
./sieve_go 10000000
```

### C++

The C++ version uses the Meson build system.

1.  **Configure the build (only needs to be done once):**
    ```sh
    cd sieve_cpp
    meson setup builddir
    ```

2.  **Compile the code:**
    ```sh
    cd sieve_cpp
    meson compile -C builddir
    ```

3.  **Run the executable:**
    ```sh
    ./sieve_cpp/builddir/sieve_cpp 10000000
    ```

### Fortran

The Fortran version also uses Meson.

1.  **Configure the build (only needs to be done once):**
    ```sh
    cd sieve_fortran
    meson setup builddir
    ```

2.  **Compile the code:**
    ```sh
    cd sieve_fortran
    meson compile -C builddir
    ```

3.  **Run the executable:**
    ```sh
    ./sieve_fortran/builddir/sieve_fortran 10000000
    ```

### Rust

The Rust version uses Cargo.

1.  **Build the optimized executable:**
    ```sh
    cd sieve_rust
    cargo build --release
    ```

2.  **Run the executable:**
    ```sh
    ./sieve_rust/target/release/sieve_rust 10000000
    ```

## Running the Benchmark

The `benchmark` script in the root of the project will automatically build and run all implementations, executing each one multiple times to provide stable performance metrics. It will also ensure that the benchmark is run inside the consistent Nix development environment.

To run the full benchmark suite:
```sh
./benchmark
```
