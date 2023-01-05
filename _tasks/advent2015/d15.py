import os
from collections import defaultdict, Counter
import math

test = """Butterscotch: capacity -1, durability -2, flavor 6, texture 3, calories 8
Cinnamon: capacity 2, durability 3, flavor -2, texture -1, calories 3"""

data = defaultdict(dict)
props = set()
ingredients = set()

txt_name = __file__.split(os.sep)[-1].replace('.py', '.txt')
#for line in test.split('\n'):
for line in open(txt_name).readlines():
    line = line.strip()
    name, vals = line.split(': ')
    for val in vals.split(', '):
        prop, val = val.split(' ')
        val = int(val)
        data[name][prop] = val
        props.add(prop)
        ingredients.add(name)

props.remove('calories')

def sum_vals(vals):  # {Butterscotch:2} -> {capacity -2, durability -4}
    vals_sum = {prop: sum([data[name][prop] * cnt for name, cnt in vals.most_common()]) for prop in props}
    return Counter({prop: vals_sum[prop] for prop in props if vals_sum[prop] > 0})


def score(vals):  # Counter
    c = sum_vals(vals)
    return math.prod(c.values())


solution = Counter({ingredient: 0 for ingredient in ingredients})
for i in range(100):
    sol_eval = {}
    old_score = score(solution)
    for ingredient in ingredients:
        solution[ingredient] += 1
        if i > 50:
            sol_eval[ingredient] = score(solution)
        else:
            res = sum_vals(solution)
            sol_eval[ingredient] = list(sorted([res[prop] for prop in props]))
        solution[ingredient] -= 1
    best = max(sol_eval.values())
    for ingredient in sol_eval:
        if sol_eval[ingredient] == best:
            solution[ingredient] += 1
            break
    print(i+1, ingredient, best, solution, score(solution))

print(solution)
print(score(solution))
"""
s = Counter({'Cinnamon': 56, 'Butterscotch': 44})
s2 = sum_vals(s)
print(s2)
print(list(sorted([s2[prop] for prop in props])))
print(score(s))
print(score(solution) == score(s))
print(score(solution) > score(s))
"""

# part 2


"""
mxs = Counter()
c = 8
for c1 in range(c):
    for c2 in range(c):
        for c3 in range(c):
            for c4 in range(c):
                s = sum([c1, c2, c3, c4])
                solution = Counter({
                    'Frosting': c1,
                    'Candy': c2,
                    'Butterscotch': c3,
                    'Sugar': c4,
                })
                mxs[s] = max(mxs[s], score(solution))

for i in range(15):
    print(i, mxs[i])
"""

calories = Counter({ingredient: data[ingredient]['calories'] for ingredient in ingredients})
vals = calories.most_common()


c = 0
cc = 0
c_= 0
calorieslst = []
scores = []
recipes = []
def iterate(solution, vals, budget):
    global c, cc, c_, scores, calorieslst, recipes
    if len(vals) == 0:
        c += 1
        if budget == 0 and sum(solution.values()) == 100:
            cc += 1
            scores.append(score(solution))
            calorieslst.append(budget)
            recipes.append((score(solution), sum(solution.values()), Counter(solution)))
        return
    name, calories = vals[0]
    for cnt in range(min(100, budget // calories + 5)):
        solution[name] = cnt
        new_budget = budget - cnt * calories
        if new_budget < 0:
            c_ -= 1
        iterate(solution, vals[1:], new_budget)

iterate(Counter(), vals, 500)
print(c, cc, c_)
print(list(sorted(scores))[-10:])
print(list(sorted(recipes, key=lambda v: v[0]))[-10:])
print(max(scores))
