from collections import defaultdict, Counter
import parse
import os

test = """fill"""

txt_name = __file__.split(os.sep)[-1].replace('.py', '.txt')
for line in test.split('\n'):
#for line in open(txt_name).readlines():
    line = line.strip()
    v = parse.parse('{} {:d}', line)

print(None)

# part 2
