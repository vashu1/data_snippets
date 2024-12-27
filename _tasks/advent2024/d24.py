from collections import defaultdict

lines = '''x00: 1
x01: 1
x02: 1
y00: 0
y01: 1
y02: 0

x00 AND y00 -> z00
x01 XOR y01 -> z01
x02 OR y02 -> z02'''
lines = '''x00: 1
x01: 0
x02: 1
x03: 1
x04: 0
y00: 1
y01: 1
y02: 1
y03: 1
y04: 1

ntg XOR fgs -> mjb
y02 OR x01 -> tnw
kwq OR kpj -> z05
x00 OR x03 -> fst
tgd XOR rvg -> z01
vdt OR tnw -> bfw
bfw AND frj -> z10
ffh OR nrd -> bqk
y00 AND y03 -> djm
y03 OR y00 -> psh
bqk OR frj -> z08
tnw OR fst -> frj
gnj AND tgd -> z11
bfw XOR mjb -> z00
x03 OR x00 -> vdt
gnj AND wpb -> z02
x04 AND y00 -> kjc
djm OR pbm -> qhw
nrd AND vdt -> hwm
kjc AND fst -> rvg
y04 OR y02 -> fgs
y01 AND x02 -> pbm
ntg OR kjc -> kwq
psh XOR fgs -> tgd
qhw XOR tgd -> z09
pbm OR djm -> kpj
x03 XOR y03 -> ffh
x00 XOR y04 -> ntg
bfw OR bqk -> z06
nrd XOR fgs -> wpb
frj XOR qhw -> z04
bqk OR frj -> z07
y03 OR x01 -> nrd
hwm AND bqk -> z03
tgd XOR rvg -> z12
tnw OR pbm -> gnj'''
lines = lines.split('\n')
lines = [i.strip() for i in open('inputs/d24.txt').readlines()]


def calc(f, op1, op2):
	if f == 'AND':
		return op1 & op2
	elif f == 'OR':
		return op1 | op2
	elif f == 'XOR':
		return op1 ^ op2
	else:
		assert False


gates_op1 = defaultdict(set)
gates_op2 = defaultdict(set)
activated_wires = {}
empty_index = lines.index('')
for i in range(empty_index):
	line = lines[i]
	inp, val = line.split(': ')
	val = int(val)
	activated_wires[inp] = val

for i in range(empty_index+1, len(lines)):
	line = lines[i]
	op1, f, op2, _, res = line.split(' ')
	gate = (op1, f, op2, res)
	gates_op1[op1].add(gate)
	gates_op2[op2].add(gate)

wires = dict(activated_wires)
while activated_wires:
	wire, value = activated_wires.popitem()
	for gate in gates_op1[wire].union(gates_op2[wire]):
		op1, f, op2, res = gate
		#print('--')
		#print(gates_op1)
		#print(gates_op2)
		#print(gate, wires, activated_wires)
		if op1 in wires and op2 in wires:
			gates_op1[op1].remove(gate)
			gates_op2[op2].remove(gate)
			v = calc(f, wires[op1], wires[op2])
			activated_wires[res] = v
			wires[res] = v

res = 0
for index, wire in enumerate(sorted([i for i in wires.keys() if i.startswith('z')])):
	flag = 1 << index
	if wires[wire]:
		res ^= flag

print(res)


# II


'''

dhb XOR qpp -> z01
y00 AND x00 -> dhb
qpp AND dhb -> ndg



y00 AND x00 -> dhb
y00 XOR x00 -> z00



y01 AND x01 -> pbr
x01 XOR y01 -> qpp
ndg OR pbr -> vnb
dhb XOR qpp -> z01
qpp AND dhb -> ndg



y44 AND x44 -> btg
x44 XOR y44 -> pfm

wmr OR btg -> z45
pfm XOR jcr -> z44
pfm AND jcr -> wmr
'''
