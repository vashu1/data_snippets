import itertools
from collections import defaultdict

input = [line.strip() for line in open('test1').readlines()]

code = {
  0: list('abcefg'), # 6
  1: list('cf'),        # 2
  2: list('acdeg'),  # 5
  3: list('acdfg'),  # 5
  4: list('bcdf'),      # 4
  5: list('abdfg'),  # 5
  6: list('abdefg'), # 6
  7: list('acf'),       # 3
  8: list('abcdefg'),   # 7
  9: list('abcdfg'), #6
}

encodings = []  # all wire combinations -> number to wire encodings
inp_wires = list('abcdefg')
for out_wires in itertools.permutations(inp_wires):
  wire_pairs = {k:v for k, v in zip(inp_wires, out_wires)}
  code2 = defaultdict(str)
  for i in range(10):
    for w in code[i]:
      code2[i] += wire_pairs[w]
  codes = {''.join(sorted(code2[k])):k for k in code2}
  encodings.append(codes)


def guess_line(line):
  inp, out = line.split(' | ')
  inp = inp.split(' ')
  inp = [''.join(sorted(v)) for v in inp]
  out = out.split(' ')
  out = [''.join(sorted(v)) for v in out]
  for encoding in encodings:
    good = True
    for v in (inp + out):
      if v not in encoding:
        good = False
        break
    if good:
      break
  return int(''.join([str(encoding[v]) for v in out]))


print(sum([guess_line(line) for line in input]))