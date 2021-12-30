# https://projecteuler.net/problem=770

def strategy(x, n, take_countdown=None, give_countdown=None):
    if take_countdown is None:
        take_countdown = n
    if give_countdown is None:
        give_countdown = n
    if take_countdown == 0 and give_countdown == 0:
        return x
    if take_countdown == 0:
        return x
    if give_countdown == 0:
        return x
    ???

'''
x = 1

n=0  -> 1
n=1  -> 1
n=2  -> 1
'''
