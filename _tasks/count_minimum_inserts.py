# minimum add to make equal
# A = [1,3,4,2,5,6] B= [3,4,6,5,7] https://careercup.com/question?id=5736582460473344
# we have to remove 3,1,2,6 from A and add 6,7 to A to make A equal B
# return minimum number of inserts
# len(A) < 1e5
# len(B) < 1e5
# A[i] < 1e9
# B[i] < 1e9
# len(B) == len(set(B)) - B elements are distinct

from bisect import bisect_left

def count_minimum_inserts(A, B):
    convert_B_elems_to_index = dict(map(reversed, enumerate(B))) # {elem -> indx}
    converted_A = [convert_B_elems_to_index[elem] for elem in A if elem in convert_B_elems_to_index]
    # converted_A = map(lambda x: convert_B_elems_to_index[x], filter(lambda x: x in convert_B_elems_to_index, A))
    piles = [] # Longest increasing subsequence via patience sorting
    for elem in converted_A:
        indx = bisect_left(piles, elem)
        if indx == len(piles):
            piles.append(elem)
        else:
            piles[indx] = elem
    return len(B) - len(piles)

assert count_minimum_inserts([1,3,4,2,5,6], [3,4,6,5,7]) == 2
print('OK')