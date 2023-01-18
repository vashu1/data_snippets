from collections import Counter, defaultdict
import os

test = '''abba[mnop]qrst
abcd[bddb]xyyx
aaaa[qwer]tyui
ioxxoj[asdfgh]zxcvbn'''  # 1001

test = '''aba[bab]xyz
xyx[xyx]xyx
aaa[kek]eke
zazbz[bzb]cdb'''


def abba(s):
    assert len(s) == 4
    return s[0] != s[1] and s[0] == s[-1] and s[1] == s[-2]


def has_abba(s):
    for i in range(len(s) + 1 - 4):
        if abba(s[i: i + 4]):
            return True
    return False


res = defaultdict(Counter)

tls = 0
ssl = 0

txt_name = __file__.split(os.sep)[-1].replace('.py', '.txt')
#for line in test.split('\n'):
for line in open(txt_name).readlines():
    aba = set()
    bab = set()
    line = line.strip()
    # validate brackets
    stack = []
    for c in line:
        if c == '[':
            stack.append('[')
        elif c == ']':
            assert stack
            _ = stack.pop()
    assert not stack
    #
    line = line.replace('[', ']-')
    seqs = []
    squares = []
    for s in line.split(']'):
        if s.startswith('-'):
            s = s[1:]
            squares.append(has_abba(s))
            for i in range(len(s) + 1 - 3):
                bab.add(s[i:i+3])
        else:
            seqs.append(has_abba(s))
            for i in range(len(s) + 1 - 3):
                aba.add(s[i:i+3])
    if any(seqs) and not any(squares):
        tls += 1
    for aba_ in aba:
        if aba_[0] != aba_[1] and aba_[0] == aba_[2]:
            if (aba_[1] + aba_[0] + aba_[1]) in bab:
                #print(line, aba_, bab)
                ssl += 1
                break

print(tls)
print(ssl)