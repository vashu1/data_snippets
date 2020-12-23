# add strings as binary

def add(a: str, b: str) -> str:
    res = []
    carry_flag = '0'
    max_len = max(len(a), len(b))
    a = reversed(a.zfill(max_len)) # pad with zeroes and invert
    b = reversed(b.zfill(max_len))
    for n1, n2 in zip(a, b): # iterate from lowest digits
        if n1 == n2: # 00 or 11 cases
            res.append(carry_flag)
            carry_flag = n1
        else: # 10 or 10 cases
            res.append('0' if carry_flag == '1' else '1')
    if carry_flag == '1': # add carry if it is set
        res.append('1')
    return ''.join(reversed(res)) # reverse and join to str

assert add('0', '0') == '0'
assert add('0', '1') == '1'
assert add('1', '1') == '10'
assert add('0', '10') == '10'
assert add('1', '10') == '11'
assert add('1', '11')  == '100'
assert add('10', '10') == '100'
assert add('11', '11') == '110'
assert add('1'+'0'*1000, '1') == '1'+'0'*999 + '1'
assert add('1'+'0'*1000, '1'+'0'*1000) == '1'+'0'*1001
print('OK')