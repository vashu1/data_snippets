# words for speaking practice - most similar ones with similar sounding letters like l-rs
import heapq
# https://github.com/hingston/russian
words = [i.strip().lower() for i in open('10000-russian-words-cyrillic-only.txt').readlines()]
# а, я, у, ю, о, е, ё, э, и, ы
rs = [i for i in words if 'р' in i and 'л' not in i]
ls = [i for i in words if 'л' in i and 'р' not in i]

def _score(r, l):
  c = 0
  for a, b in zip(r, l):
    if a == b:
      c += 1
  return c

def score(r, l):
  c = max(_score(r, l), _score(r, ' ' + l), _score(' ' + r, l), _score(r, '  ' + l), _score('  ' + r, l))
  return c / max(len(r), len(l))

c = 0
top = []
for r in rs:
  for l in ls:
    c += 1
    if c % 100_000 == 0:
      print(c)
    ri = r.find('р')
    li = l.find('л')
    rstr = r[ri+1:]
    lstr = l[li+1:]
    if rstr and lstr and rstr[0] == lstr[0]:
      continue
    heapq.heappush(top, (-score(r, l), r, l))
    if len(top) > 2_000:
      top = top[:1_000]

for _, a, b in top[:100]:
  print(a, b)