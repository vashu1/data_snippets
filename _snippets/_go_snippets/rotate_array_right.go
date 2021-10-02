package solution

// you can also use imports, for example:
// import "fmt"
// import "os"

// you can write to stdout for debugging purposes, e.g.
// fmt.Println("this is a debug message")

func Solution(A []int, K int) []int {
    if (K == 0) || (len(A) == 0) || (K % len(A) == 0) {
        return A
    }
    K = K % len(A) // now K is below len of A
    result := make([]int, len(A))
    for i := 0 ; i < len(A) ; i++ {
        result[(i + K) % len(A)] = A[i]
    }
    return result
}
