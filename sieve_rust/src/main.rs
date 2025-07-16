use rayon::prelude::*;
use std::env;

fn main() {
    let n_str = env::args().nth(1).expect("Usage: sieve_rust <N>");
    let n: usize = n_str.parse().expect("N must be an integer");

    if n < 2 {
        println!("Found 0 primes smaller than {}", n);
        return;
    }

    let mut primes: Vec<bool> = (0..=n).map(|i| i >= 2).collect();
    let limit = (n as f64).sqrt() as usize;

    (2..=limit).for_each(|i| {
        if primes[i] {
            for multiple in (i * i..=n).step_by(i) {
                primes[multiple] = false;
            }
        }
    });

    let count = primes.par_iter().filter(|&&is_prime| is_prime).count();
    println!("Found {} primes smaller than {}", count, n);
}
