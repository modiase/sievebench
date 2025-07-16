package main

import (
	"fmt"
	"math"
	"os"
	"runtime"
	"strconv"
	"sync"
)

func main() {
	if len(os.Args) < 2 {
		fmt.Println("Usage: go run sieve.go <P>")
		fmt.Println("Calculates primes up to 10^P")
		return
	}

	pStr := os.Args[1]
	p, err := strconv.Atoi(pStr)
	if err != nil {
		fmt.Println("Invalid power:", pStr)
		return
	}
	N := int(math.Pow10(p))

	numCPU := runtime.NumCPU()
	runtime.GOMAXPROCS(numCPU)

	primes := make([]bool, N+1)
	for i := 2; i <= N; i++ {
		primes[i] = true
	}

	var wg sync.WaitGroup

	for i := 2; i*i <= N; i++ {
		if primes[i] {
			wg.Add(1)
			go func(start int) {
				defer wg.Done()
				for j := start * start; j <= N; j += start {
					primes[j] = false
				}
			}(i)
		}
	}

	wg.Wait()

	count := 0
	for i := 2; i <= N; i++ {
		if primes[i] {
			count++
		}
	}

	fmt.Printf("Found %d primes smaller than %d.\n", count, N)
}
