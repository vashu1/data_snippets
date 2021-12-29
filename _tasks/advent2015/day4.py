import hashlib
c = 0
while True:
    c += 1
    s = f'bgvyzdsv{c}'
    hsh = hashlib.md5(s.encode('utf-8')).hexdigest()
    if hsh.startswith('00000'):
        print(c)
        break

c = 0
while True:
    c += 1
    s = f'bgvyzdsv{c}'
    hsh = hashlib.md5(s.encode('utf-8')).hexdigest()
    if hsh.startswith('000000'):
        print(c)
        break