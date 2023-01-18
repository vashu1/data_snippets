from collections import Counter, defaultdict
import os

test = ''''''

res = defaultdict(Counter)

txt_name = __file__.split(os.sep)[-1].replace('.py', '.txt')
for line in test.split('\n'):
#for line in open(txt_name).readlines():
    line = line.strip()