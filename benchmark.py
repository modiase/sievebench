import subprocess
import time
import os
import statistics

def run_command(command, cwd=None):
    """Runs a command and returns the execution time."""
    start_time = time.time()
    subprocess.run(command, cwd=cwd, capture_output=True, text=True, check=True)
    end_time = time.time()
    return end_time - start_time

def print_results(results):
    """Prints the benchmark results in a formatted table."""
    print(f"{'N':<15} | {'Mean (s)':<15} | {'Best (s)':<15} | {'Std Dev (s)':<15}")
    print("-" * 68)
    for n, stats in results.items():
        mean = f"{stats['mean']:.4f}"
        best = f"{stats['best']:.4f}"
        std_dev = f"{stats['std_dev']:.4f}"
        print(f"{n:<15,} | {mean:<15} | {best:<15} | {std_dev:<15}")

def main():
    """Main function to run the benchmark and print the results."""
    n_values = [1_000_000, 10_000_000, 100_000_000]
    num_runs = 5
    
    # --- Go Benchmark ---
    print("--- Go Benchmark ---")
    print("Building Go code with optimizations...")
    go_dir = "sieve_go"
    go_executable = os.path.join(go_dir, "sieve_go")
    subprocess.run(
        ["go", "build", "-ldflags", "-s -w", "-o", "sieve_go", "."],
        cwd=go_dir,
        check=True,
        capture_output=True
    )
    
    go_results = {}
    for n in n_values:
        times = [run_command([f"./{go_executable}", str(n)]) for _ in range(num_runs)]
        go_results[n] = {
            'mean': statistics.mean(times),
            'best': min(times),
            'std_dev': statistics.stdev(times) if len(times) > 1 else 0.0
        }
    print_results(go_results)

    # --- C++ Benchmark ---
    print("\n--- C++ Benchmark ---")
    print("Building C++ code...")
    cpp_dir = "sieve_cpp"
    subprocess.run(["nix", "develop", "--command", "bash", "-c", f"cd {cpp_dir} && meson setup builddir --reconfigure"], check=True, capture_output=True)
    subprocess.run(["nix", "develop", "--command", "bash", "-c", f"cd {cpp_dir} && meson compile -C builddir"], check=True, capture_output=True)
    
    cpp_results = {}
    cpp_executable = os.path.join(cpp_dir, "builddir", "sieve_cpp")
    for n in n_values:
        times = [run_command([f"./{cpp_executable}", str(n)]) for _ in range(num_runs)]
        cpp_results[n] = {
            'mean': statistics.mean(times),
            'best': min(times),
            'std_dev': statistics.stdev(times) if len(times) > 1 else 0.0
        }
    print_results(cpp_results)

    # --- Fortran Benchmark ---
    print("\n--- Fortran Benchmark ---")
    print("Building Fortran code...")
    fortran_dir = "sieve_fortran"
    subprocess.run(["nix", "develop", "--command", "bash", "-c", f"cd {fortran_dir} && meson setup builddir --reconfigure"], check=True, capture_output=True)
    subprocess.run(["nix", "develop", "--command", "bash", "-c", f"cd {fortran_dir} && meson compile -C builddir"], check=True, capture_output=True)

    fortran_results = {}
    fortran_executable = os.path.join(fortran_dir, "builddir", "sieve_fortran")
    for n in n_values:
        times = [run_command([f"./{fortran_executable}", str(n)]) for _ in range(num_runs)]
        fortran_results[n] = {
            'mean': statistics.mean(times),
            'best': min(times),
            'std_dev': statistics.stdev(times) if len(times) > 1 else 0.0
        }
    print_results(fortran_results)

    # --- Rust Benchmark ---
    print("\n--- Rust Benchmark ---")
    print("Building Rust code with optimizations...")
    rust_dir = "sieve_rust"
    subprocess.run(
        ["nix", "develop", "--command", "bash", "-c", f"cd {rust_dir} && cargo build --release"],
        check=True,
        capture_output=True
    )
    
    rust_results = {}
    rust_executable = os.path.join(rust_dir, "target", "release", "sieve_rust")
    for n in n_values:
        times = [run_command([f"./{rust_executable}", str(n)]) for _ in range(num_runs)]
        rust_results[n] = {
            'mean': statistics.mean(times),
            'best': min(times),
            'std_dev': statistics.stdev(times) if len(times) > 1 else 0.0
        }
    print_results(rust_results)


if __name__ == "__main__":
    main()