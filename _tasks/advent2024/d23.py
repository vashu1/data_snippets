from collections import defaultdict

lines = '''kh-tc
qp-kh
de-cg
ka-co
yn-aq
qp-ub
cg-tb
vc-aq
tb-ka
wh-tc
yn-cg
kh-ub
ta-co
de-co
tc-td
tb-wq
wh-td
ta-ka
td-qp
aq-cg
wq-ub
ub-vc
de-ta
wq-aq
wq-vc
wh-yn
ka-de
kh-ta
co-tc
wh-qp
tb-vc
td-yn'''
lines = lines.split('\n')
lines = [i.strip() for i in open('inputs/d23.txt').readlines()]

connections = defaultdict(set)
for line in lines:
	a, b = line.split('-')
	connections[a].add(b)
	connections[b].add(a)

triplets = set()
for line in lines:
	a, b = line.split('-')
	thirds = connections[a].intersection(connections[b])
	for third in thirds:
		result = tuple(sorted([a, b, third]))
		if any([i.startswith('t') for i in result]):
			triplets.add(result)

print(len(triplets))


# II


import networkx as nx

G = nx.Graph()
for line in lines:
	a, b = line.split('-')
	G.add_edge(a, b)

m = max(nx.algorithms.clique.find_cliques(G), key = len)
print(','.join(sorted(m)))