'''
There is a somewhat confusing situation at the dog show this year. Four
brothers - Andy, Bill, Colin and Donald - each enter two dogs, and each
has named his dogs after two of his brothers. Consequently, there are two
dogs named Andy, two named Bill, two named Colin and two named Donald.

Of the eight dogs, three are corgis, three labradors and two dalmatians.
None of the four brothers owns two dogs of the same breed. No two dogs
of the same breed have the same name. Neither of Andy's dogs is named
Donald and neither of Colin's dogs is named Andy. No corgi is named Andy
and no labrador is named Donald. Bill does not own a Labrador.

Who are the owners of the dalmatians and what are the dalmatians' names?
'''

names = ['A','B','C','D']
breeds = ['c','l','d']
dog_types = [(i+j) for i in names for j in breeds]

from collections import defaultdict
import itertools
i = 0
results = []
for variant in itertools.product(dog_types, repeat=8):
    i+=1
    if i%1000000==0:
        print(i/1000000)
    s = ''.join(variant)
    names  = s[0::2]
    breeds = s[1::2]
    # names
    if sorted(names) != ['A','A','B','B','C','C','D','D']:
        continue
    # breed count
    if sorted(breeds) != ['c','c','c','d','d','l','l','l']:
        continue
    # names of brother and his dogs differ
    if s[0*4] == 'A' or s[1*4] == 'B' or s[2*4] == 'C' or s[3*4] == 'D': 
        continue
    if s[0*4+2] == 'A' or s[1*4+2] == 'B' or s[2*4+2] == 'C' or s[3*4+2] == 'D': 
        continue
    # no same name per brother
    if names[0*2]==names[0*2+1] or names[1*2]==names[1*2+1] or names[2*2]==names[2*2+1] or names[3*2]==names[3*2+1]:
        continue
    # no same breed per brother
    if breeds[0*2]==breeds[0*2+1] or breeds[1*2]==breeds[1*2+1] or breeds[2*2]==breeds[2*2+1] or breeds[3*2]==breeds[3*2+1]:
        continue
    # no Andys Donald
    if names[0*2] == 'D' or names[0*2+1] == 'D':
        continue
    # no colins andy
    if names[2*2] == 'A' or names[2*2+1] == 'A':
        continue
    # bill no labrador
    if breeds[1*2] == 'l' or breeds[1*2+1] == 'l':
        continue
    # no corgy Andy and no labrador Donald
    flag = False
    for n,b in zip(names,breeds):
        if b=='c' and n=='A':
            flag = True
            break
        if b=='l' and n=='D':
            flag = True
            break
    if flag:
        continue
    # no same breed same name
    breednames = defaultdict(set)
    for n,b in zip(names,breeds): 
        if n in breednames[b]:
            flag = True
            break
        breednames[b].add(n)
    if flag:
        continue
    print(s)
    results.append(s)

for s in results:
    print(s)

a = []
c = []
for s in results:
    names  = s[0::2]
    breeds = s[1::2]
    print_result = ''
    print_result2 = ''
    for indx, pair in enumerate(zip(names,breeds)):
        n,b = pair 
        if b=='d':
            print_result += n+b
            print_result2 += str(indx)
    print(print_result)
    print(print_result2)
    a.append(print_result)
    c.append(print_result2)

print(set(a))
print(set(c))
# set(['DdAd', 'AdDd'])

"""
sympy logical reasosning
https://docs.sympy.org/latest/modules/logic.html

 function1 = SOPform([x, z, y],[[1, 0, 1], [0, 0, 1]])
 
 >>> minterms = [[0, 0, 0, 1], [0, 0, 1, 1],
...             [0, 1, 1, 1], [1, 0, 1, 1], [1, 1, 1, 1]]
dontcares = [0, 2, 5]
SOPform([w, x, y, z], minterms, dontcares)

$ cat _python_snippets/SAT_solver.py
https://habr.com/ru/post/440092/
https://colab.research.google.com/drive/1Fk4Vncc3Q9Ghxu1Of9Y8KUtlHPqPYymV
https://github.com/z3prover/z3
"""