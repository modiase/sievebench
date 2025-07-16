use rayon::prelude::*;
use std::env;

fn main() {
    let p_str = env::args().nth(1).expect("Usage: sieve_rust <P> (calculates primes up to 10^P)");
    let p: u32 = p_str.parse().expect("P must be an integer");
    let n: usize = (10 as usize).pow(p);

    if n < 2 {
        println!("Found 0 primes smaller than 10^{}", p);
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
