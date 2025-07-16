package main

import (
	"fmt"
	"os"
	"runtime"
	"strconv"
	"sync"
)

func main() {
	if len(os.Args) < 2 {
		fmt.Println("Usage: go run sieve.go <N>")
		return
	}

	nStr := os.Args[1]
	N, err := strconv.Atoi(nStr)
	if err != nil {
		fmt.Println("Invalid number:", nStr)
		return
	}

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
