package solution

// longest gap of 0s in N

// you can also use imports, for example:
//import "fmt"
// import "os"

// you can write to stdout for debugging purposes, e.g.
// fmt.Println("this is a debug message")

func Solution(N int) int {
    var position uint8 = 0
    // skip initial zeroes
    for ; (position < 31) && (((1 << position) & N) == 0); position++ {}
    // now position points to digit 1 or end of N
    max_consecutive_0s := 0
    current_consecutive_0s := 0
    // search for sequences of 0s
    for ; position < 31; position++ { 
        current_digit := (1 << position) & N
        if current_digit > 0  {
            if current_consecutive_0s > max_consecutive_0s {
                max_consecutive_0s = current_consecutive_0s
            }
            current_consecutive_0s = 0
        } else {// current digit is 0
            current_consecutive_0s++
        }
    }
    return max_consecutive_0s
}

