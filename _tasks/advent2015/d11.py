psw = 'vzbxkghb'


def is_valid(p):
    """
    exactly eight lowercase letters
    """
    if not len(p) == 8:
        return False
    if not p.islower():
        return False
    if not p.isalpha():
        return False
    """
    # Passwords must include one increasing straight of at least three letters, like abc, bcd, cde, and so on, up to xyz.
    # They cannot skip letters; abd doesn't count.
    """
    triplets = [(ord(a), ord(b), ord(c)) for a, b, c in zip(p, p[1:], p[2:])]
    diffs = [(b - a, c - b) for a, b, c in triplets]
    if (1, 1) not in diffs:
        return False
    """
    Passwords may not contain the letters i, o, or l, as these letters can be mistaken for other characters
    """
    for i in 'iol':
        if i in p:
            return False
    """
    Passwords must contain at least two different, non-overlapping pairs of letters, like aa, bb, or zz.
    """
    pairs = set([(c1 + c2) for c1, c2 in zip(p, p[1:]) if c1 == c2])
    if len(pairs) < 2:
        return False
    return True


def inc_not_z(c):
    return chr(ord(c) + 1)


def inc(v):
    if v == 'z' * 8:
        return 'a' * 8
    for i in range(7, 0-1, -1):
        if v[i] != 'z':
            return v[:i] + inc_not_z(v[i]) + ('a' * (7 - i))
    assert False


def next_psw(p):
    print(is_valid(p))
    c = 0
    p = inc(p)
    while not is_valid(p):
        p = inc(p)
        c += 1
    print(c, p)
    return p


psw = next_psw(psw)

psw = next_psw(psw)