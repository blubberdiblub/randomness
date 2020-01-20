package main

import (
	"fmt"
	"gonum.org/v1/gonum/floats"
	"gonum.org/v1/gonum/mathext"
	"gonum.org/v1/gonum/stat"
	"gonum.org/v1/gonum/stat/distuv"
	"math"
	"math/rand"
	"sort"
	"time"
)

const (
	M       = 4096
	N       = 1 << 32
	NumRuns = 5000
)

func chi2Lambda(m uint, n int) float64 {
	return math.Pow(float64(m), 3) / (4 * float64(n))
}

func getExpected(m uint, n int, numRuns uint) []float64 {
	lam := chi2Lambda(m, n)
	reversalPoint := uint(math.Ceil(lam))
	running := math.Exp(-lam) * float64(numRuns)

	expected := make([]float64, m)
	expected[0] = running
	remainder := float64(numRuns)

	for k := uint(0); k < m; k++ {
		nextRemainder := remainder - running
		if k > reversalPoint && (running < 15 || nextRemainder < 15) {
			expected[k] = remainder
			return expected[:k + 1]
		}

		expected[k] = running
		running *= lam / float64(k + 1)
		remainder = nextRemainder
	}

	return expected
}

func bday(r *rand.Rand, m uint, n int, numRuns uint) []uint {
	if numRuns <= 0 { panic("numRuns must be >= 1") }
	if n <= 0 { panic("n must be >= 1") }
	if m <= 0 { panic("m must be >= 1") }

	distribution := make([]uint, m + 1)

	birthdays := make([]int, m)
	spacings := make([]int, m)

	for rep := uint(0); rep < numRuns; rep++ {
		for i := range birthdays {
			birthdays[i] = r.Intn(n)
		}

		sort.Ints(birthdays)

		for i, a := range birthdays[1:] {
			spacings[i] = a - birthdays[i]
		}
		spacings[m - 1] = birthdays[0] + int(n) - birthdays[m - 1]

		sort.Ints(spacings)

		var last int = -1
		var countUnique uint = 0

		for _, s := range spacings {
			if s != last {
				countUnique += 1
			}
			last = s
		}

		distribution[m - countUnique]++
	}

	return distribution
}

func changeLength(s []float64, l int) []float64 {
	if l == len(s) {
		return s
	}

	if l <= 0 {
		panic("illegal length")
	}

	n := make([]float64, l)
	if l >= len(s) {
		copy(n, s)
	} else {
		sumIndex := l - 1
		copy(n[:sumIndex], s)
		n[sumIndex] = floats.Sum(s[sumIndex:])
	}

	return n
}

func minInt(a, b int) int {
	if a <= b {
		return a
	}

	return b
}

func main() {
	fmt.Printf("lambda = %f\n", chi2Lambda(M, N))

	expected := getExpected(M, N, NumRuns)
	fmt.Println(expected[:minInt(len(expected), 30)])

	observed := []float64{87, 385, 748, 962, 975, 813, 472, 308, 159, 61, 30}
	observed = changeLength(observed, len(expected))
	fmt.Println(observed[:minInt(len(expected), 30)])

	dist := stat.ChiSquare(observed, expected)
	fmt.Println(dist)

	pvalue := mathext.GammaInc(float64(len(expected) - 1) * 0.5, dist* 0.5)
	fmt.Println(pvalue)

	myChiSquared := distuv.ChiSquared{K: float64(len(expected) - 1), Src: nil}
	fmt.Println(myChiSquared.CDF(dist))
	fmt.Println(myChiSquared.Survival(dist))

	r := rand.New(rand.NewSource(1))

	started := time.Now()
	distribution := bday(r, M, N, NumRuns)
	elapsed := time.Since(started)

	fmt.Printf("took %v\n", elapsed)
	fmt.Println(distribution[:40])
}
