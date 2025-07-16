#include <iostream>
#include <vector>
#include <thread>
#include <numeric>
#include <algorithm>
#include <cmath>

void sieve_worker(std::vector<char>& primes, int start, int end) {
    for (int p = start; p <= end; ++p) {
        if (primes[p]) {
            for (long long i = (long long)p * p; i < primes.size(); i += p) {
                primes[i] = 0;
            }
        }
    }
}

int main(int argc, char* argv[]) {
    if (argc < 2) {
        std::cerr << "Usage: " << argv[0] << " <P>" << std::endl;
        std::cerr << "Calculates primes up to 10^P" << std::endl;
        return 1;
    }

    int p = std::atoi(argv[1]);
    long long n = static_cast<long long>(std::pow(10, p));

    if (n <= 1) {
        return 0;
    }

    unsigned int num_threads = std::thread::hardware_concurrency();
    // Use std::vector<char> instead of std::vector<bool> to avoid the memory-optimized
    // specialization of std::vector<bool>, which can cause false sharing and hurt
    // performance in a concurrent context. Each char acts as a byte-sized boolean.
    std::vector<char> primes(n + 1, 1);
    primes[0] = primes[1] = 0;

    std::vector<std::thread> threads;
    int limit = static_cast<int>(std::sqrt(n));
    int step = (limit - 2) / num_threads;
    if (step == 0) step = 1;

    for (unsigned int i = 0; i < num_threads; ++i) {
        int start = 2 + i * step;
        int end = (i == num_threads - 1) ? limit : start + step - 1;
        if (start > limit) break;
        threads.emplace_back(sieve_worker, std::ref(primes), start, end);
    }

    for (auto& t : threads) {
        t.join();
    }

    long long count = 0;
    for (int i = 2; i <= n; ++i) {
        if (primes[i]) {
            count++;
        }
    }

    std::cout << "Found " << count << " primes smaller than " << n << "." << std::endl;

    return 0;
}
