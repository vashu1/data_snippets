import hashlib

data = 'uqwqemis'
#data = 'abc'

psw = []
indx = 0
while len(psw) < 8:
    v = data + str(indx)
    hx = hashlib.md5(v.encode('utf-8')).hexdigest()
    if hx.startswith('00000'):
        print(hx, hx[6-1])
        psw.append(hx[6-1])
    indx += 1

print(''.join(psw))
print('\n\nPART II')

psw = ['?'] * 8
guessed = 0
indx = 0
while guessed < 8:  # any([(c=='?') for c in psw]):
    if indx % 1_000_000 == 0:
        print(indx)
    v = data + str(indx)
    hx = hashlib.md5(v.encode('utf-8')).hexdigest()
    if hx.startswith('00000'):
        p = hx[6 - 1]
        if p in '01234567':
            p = int(p)
            c = hx[7 - 1]
            if psw[p] == '?':
                psw[p] = c
                print(psw, p, c)
                guessed += 1
    indx += 1

print(''.join(psw))
