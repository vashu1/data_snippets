#include <stdio.h>
#include <string.h>

inline void invert_interval(char *s, size_t start, size_t end) { // s[end] is not processed, only s[end-1]
	for (char *first = &s[start], *second = &s[end - 1], temp; first < second ; first++, second--) {
    	temp = *first;
        *first = *second;
        *second = temp;
    }
}

void invert_words(char *s) { // "ab cd" -> invert all string "dc ba" -> invert words "cd ba"
    size_t word_end;
    for (size_t word_start = 0, word_end = 0; s[word_end] != '\0' ; word_end++)
        if (s[word_end] == ' ' || word_end == str_len) { 
            invert_interval(s, word_start, word_end);
            word_start = word_end + 1;
        }
    invert_interval(s, 0, word_end);
}

void test(char *str) {
	char test[100];
	strcpy(test, str);
	invert_words(test);
	printf("'%s': '%s'\n", str, test);
}

int main() {
    test("");
    test("ab");
    test("ab cd");
    test("ab cd   ef");
    test("    abc  def ");
    return 0;
}
