A DNA sequence can be represented as a string consisting of the letters A, C, G and T, which correspond to the types of successive nucleotides in the sequence. Each nucleotide has an impact factor, which is an integer. Nucleotides of types A, C, G and T have impact factors of 1, 2, 3 and 4, respectively. You are going to answer several queries of the form: What is the minimal impact factor of nucleotides contained in a particular part of the given DNA sequence?

The DNA sequence is given as a non-empty string S = S[0]S[1]...S[N-1] consisting of N characters. There are M queries, which are given in non-empty arrays P and Q, each consisting of M integers. The K-th query (0 ≤ K < M) requires you to find the minimal impact factor of nucleotides contained in the DNA sequence between positions P[K] and Q[K] (inclusive).

For example, consider string S = CAGCCTA and arrays P, Q such that:

    P[0] = 2    Q[0] = 4
    P[1] = 5    Q[1] = 5
    P[2] = 0    Q[2] = 6
The answers to these M = 3 queries are as follows:

The part of the DNA between positions 2 and 4 contains nucleotides G and C (twice), whose impact factors are 3 and 2 respectively, so the answer is 2.
The part between positions 5 and 5 contains a single nucleotide T, whose impact factor is 4, so the answer is 4.
The part between positions 0 and 6 (the whole string) contains all nucleotides, in particular nucleotide A whose impact factor is 1, so the answer is 1.
Write a function:

func Solution(S string, P []int, Q []int) []int

that, given a non-empty string S consisting of N characters and two non-empty arrays P and Q consisting of M integers, returns an array consisting of M integers specifying the consecutive answers to all queries.

Result array should be returned as an array of integers.

For example, given the string S = CAGCCTA and arrays P, Q such that:

    P[0] = 2    Q[0] = 4
    P[1] = 5    Q[1] = 5
    P[2] = 0    Q[2] = 6
the function should return the values [2, 4, 1], as explained above.

Write an efficient algorithm for the following assumptions:

N is an integer within the range [1..100,000];
M is an integer within the range [1..50,000];
each element of arrays P, Q is an integer within the range [0..N − 1];
P[K] ≤ Q[K], where 0 ≤ K < M;
string S consists only of upper-case English letters A, C, G, T.




package solution

// you can also use imports, for example:
// import "fmt"
// import "os"

// you can write to stdout for debugging purposes, e.g.
// fmt.Println("this is a debug message")

import (
	//"fmt"
	"sort"
)


type Slice struct {
	sort.IntSlice
	idx []int
}

func (s Slice) Swap(i, j int) {
	s.IntSlice.Swap(i, j)
	s.idx[i], s.idx[j] = s.idx[j], s.idx[i]
}

func NewSlice(n []int) *Slice {
	s := &Slice{IntSlice: sort.IntSlice(n), idx: make([]int, len(n))}
	for i := range s.idx {
		s.idx[i] = i
	}
	sort.Sort(s)
	return s
}

func Solution(S string, P []int, Q []int) []int {
    impact_map := map[rune]int{
        'A':   1,
        'C':   2,
        'G':   3,
        'T':   4,
    }
    M := len(P)
    starts := NewSlice(P)
    ends   := NewSlice(Q)
    current_start := 0
    current_end   := 0
    query_results_arr := make([]int, M)
    current_queries := make(map[int]map[int]bool) // impact -> query index set
    for i := 1; i <= 4; i++ { // init nested maps
        current_queries[i] = make(map[int]bool)
    }
    //fmt.Println("starts", starts.IntSlice, "idx", starts.idx)
    //fmt.Println("ends", ends.IntSlice, "idx", ends.idx)
    for indx, ch := range S {
        //fmt.Println("indx", indx, "ch", ch)
        impact := impact_map[ch]
        // add new queries
        for ; current_start < M && starts.IntSlice[current_start] == indx ; current_start++ {
            query_id := starts.idx[current_start]
            current_queries[impact][query_id] = true
            //fmt.Println("add query", query_id, "impact", impact)
        }
        //fmt.Println("current_queries", current_queries)
        // change min current for queries
        for i := 4; i > impact; i-- {
            if len(current_queries[i]) > 0 {
                for query_id := range current_queries[i] {
                    delete(current_queries[i], query_id)
                    current_queries[impact][query_id] = true
                }
            }
        }
        //fmt.Println("current_queries", current_queries)
        // drop finished queries
        for ; current_end < M && ends.IntSlice[current_end] == indx ; current_end++ {
            query_id := ends.idx[current_end]
            for current_impact := 1; current_impact <= 4; current_impact++ {
                if _, ok := current_queries[current_impact][query_id]; ok {
                    delete(current_queries[current_impact], query_id)
                    query_results_arr[query_id] = current_impact
                    //fmt.Println("drop query", query_id, "impact", current_impact)
                }
            }
        }
    }
    return query_results_arr
}


package solution

// you can also use imports, for example:
// import "fmt"
// import "os"

// you can write to stdout for debugging purposes, e.g.
// fmt.Println("this is a debug message")

func Solution(S string, P []int, Q []int) []int {
    N := len(S)
    M := len(P)
    // create index
    index := make([][]int, 4)
    for impact := 0; impact < 4; impact++ {
        index[impact] = make([]int, N+1)
    }
    for indx, ch := range S {
        for impact := 0; impact < 4; impact++ {
            index[impact][indx+1] = index[impact][indx]
        }
        switch ch {
            case 'A':
                index[0][indx+1]++
            case 'C':
                index[1][indx+1]++
            case 'G':
                index[2][indx+1]++
            case 'T':
                index[3][indx+1]++
        }
    }
    // fill out result
    result := make([]int, M)
    for indx := 0; indx < M; indx++ {
        start := P[indx]
        end   := Q[indx]
        //fmt.Println("-",indx,start,end)
        for impact := 0; impact < 4; impact++ {
            count := index[impact][end+1] - index[impact][start]
            //fmt.Println("==",impact,count)
            if count > 0 {
                result[indx] = impact + 1
                break
            }
        }
    }
    return result
}

=== KOTLIN

fun solution(S: String, P: IntArray, Q: IntArray): IntArray {
    val allowedChars = listOf('A', 'C', 'G', 'T')
    val stringToIndexForLetter = {s: String, letter: Char -> 
        s
        .map{if (it == letter) 1 else 0}
        .fold(mutableListOf(0)) 
            {acc, elem -> acc.also({acc.add(acc.last()+elem)})}
    }
    val indexes = allowedChars.map{stringToIndexForLetter(S, it)}
    val M = P.size
    return (0 until M).map {indx ->
            (0 until allowedChars.size)
                .map {indexes[it][Q[indx]+1] - indexes[it][P[indx]]}
                .indexOfFirst{it > 0}
        }.map{it + 1}.toIntArray()
}
