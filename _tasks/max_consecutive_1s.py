# array of 1 and 0
# find max number of consecutive 1
# if you can flip k bits - find max consecutive 1s

def max_consecutive_1s(arr):
    max_count = current_count = 0
    for i in arr:
        if i: # 1s sequence goes on
            current_count += 1
        elif current_count: # 0s sequence started
            max_count = max(current_count, max_count)
            current_count = 0
    return max(current_count, max_count)

def max_consecutive_1s(arr):
    str_arr = ''.join(map(str, arr))
    return max(map(len, str_arr.split('0')))

assert max_consecutive_1s([]) == 0
assert max_consecutive_1s([0]) == 0
assert max_consecutive_1s([1]) == 1
assert max_consecutive_1s([1,0,1,1]) == 2
assert max_consecutive_1s([0,1,1,0,1]) == 2

def forward(arr, indx):
    if indx == len(arr):
        return indx, 0
    new_indx = indx + 1
    while new_indx < len(arr) and arr[new_indx] == arr[new_indx - 1]:
        new_indx  += 1
    return new_indx, new_indx - indx # new index and count of last sequence elements, new_indx points to start of new sequence or equals len(arr)

assert forward([1], 1) == (1,0)
assert forward([1,1,1], 0) == (3,3)
assert forward([1,1,0], 0) == (2,2)
assert forward([1,1,1], 1) == (3,2)
assert forward([1,1,0], 1) == (2,1)

def max_consecutive_1s_if_flipped_k(arr, k):
    if not arr:
        return 0
    start_indx = end_indx = total_1s_count = current_k = 0
    if not arr[0]: # starts with 0s
        start_indx, _ = forward(arr, start_indx) # now start_indx always points to 1s
    end_indx, _ = forward(arr, start_indx)       # now end_indx points at 0s after start_indx
    while True:
        while current_k <= k: # forward end_indx
            total_1s_count = max(total_1s_count, end_indx - start_indx)
            if end_indx == len(arr):
                return total_1s_count
            end_indx, count_0s = forward(arr, end_indx)
            end_indx, _ = forward(arr, end_indx) # now end_indx again points to start of 0s sequence of end of arr
            current_k += count_0s
        # forward start_index
        start_indx, _ = forward(arr, start_indx)
        start_indx, count_0s = forward(arr, start_indx)# now end_indx again points to start of 1s sequence
        current_k -= count_0s

assert max_consecutive_1s_if_flipped_k([1,0,1,1],0) == 2
assert max_consecutive_1s_if_flipped_k([1,0,1,1],1) == 4
assert max_consecutive_1s_if_flipped_k([1,0,0,1],1) == 1
assert max_consecutive_1s_if_flipped_k([1,0,1,1],2) == 4
assert max_consecutive_1s_if_flipped_k([0,1,0,0,1,1,0],2) == 5
assert max_consecutive_1s_if_flipped_k([0,1,0,0,0,1,1],2) == 2
assert max_consecutive_1s_if_flipped_k([0,1,0,0,0,1,1,0,0,0,0,1],2) == 2
print('OK')