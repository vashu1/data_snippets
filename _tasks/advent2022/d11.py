import math

input_test = """Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3

Monkey 1:
  Starting items: 54, 65, 75, 74
  Operation: new = old + 6
  Test: divisible by 19
    If true: throw to monkey 2
    If false: throw to monkey 0

Monkey 2:
  Starting items: 79, 60, 97
  Operation: new = old * old
  Test: divisible by 13
    If true: throw to monkey 1
    If false: throw to monkey 3

Monkey 3:
  Starting items: 74
  Operation: new = old + 3
  Test: divisible by 17
    If true: throw to monkey 0
    If false: throw to monkey 1"""
input_test = input_test.split('\n')

input_full = open('d11.txt').readlines()

input = [l.strip() for l in input_full]

class Monkey:
    def __init__(self, items, operation, test_div, action_true, action_false):
        self.items = items
        self.operation = operation
        self.test_div = test_div
        self.action_true = action_true
        self.action_false = action_false

    def empty_copy(self):
        return Monkey([], self.operation, self.test_div, self.action_true, self.action_false)

    def parse(input):
        indx = 0
        monkeys = []
        while indx < len(input):
            assert input[indx].startswith('Monkey ')
            items = [int(i.strip()) for i in input[indx+1].split(':')[1].split(',')]
            operation = eval('lambda old:' + input[indx+2].split('=')[1])
            test_div = int(input[indx+3].split(' ')[-1])
            action_true = int(input[indx+4].split(' ')[-1])
            action_false = int(input[indx + 5].split(' ')[-1])
            monkeys.append(Monkey(items, operation, test_div, action_true, action_false))
            indx += 7
        return monkeys


monkeys = Monkey.parse(input)

inspections = [0]*len(monkeys)
for round in range(20):
    for indx, m in enumerate(monkeys):
        inspections[indx] += len(m.items)
        items = m.items
        m.items = []
        for item in items:
            new_worry = m.operation(item)
            new_worry //= 3
            throw_to_indx = m.action_true if new_worry % m.test_div == 0 else m.action_false
            monkeys[throw_to_indx].items.append(new_worry)

inspections.sort()
print(inspections[-1] * inspections[-2])

# PART II

monkeys = Monkey.parse(input)

inspections = [0]*len(monkeys)
monkey_div = math.prod([m.test_div for m in monkeys])

for round in range(10_000):
    for indx, m in enumerate(monkeys):
        inspections[indx] += len(m.items)
        items = m.items
        m.items = []
        for item in items:
            new_worry = m.operation(item)
            new_worry %= monkey_div
            throw_to_indx = m.action_true if new_worry % m.test_div == 0 else m.action_false
            monkeys[throw_to_indx].items.append(new_worry)

inspections.sort()
print(inspections[-1] * inspections[-2])