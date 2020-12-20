# book source https://github.com/TheBrain0110/worm_scraper then convert it from mobi to txt online
from collections import Counter, defaultdict

def line2words(line):
    text = line.strip().lower()
    words = []
    for c in text:
        words.append(c if c.isalpha() else ' ')
    words = ''.join(words)
    return words.split(' ')

lines = open('worm.txt').readlines()

chapters = []
for line in lines[2:609]:
    if not line.strip():
        continue
    chapters.append(line)

chapters.append('Table of Contents')

chapter2words = defaultdict(Counter)
indx = 0
for line in lines[610:]:
    if line == chapters[indx]:
        print(indx, chapters[indx].strip())
        indx += 1
        if indx == len(chapters):
            break
        continue
    if indx == 0:
        continue
    for word in line2words(line):
        chapter2words[chapters[indx-1]][word] += 1

all = Counter()
for chapter in chapter2words:
    all += chapter2words[chapter]

# >>> max([len(c) for c in chapters])
# 34
exclude = set([word for word, _ in all.most_common(100)])
for chapter in chapter2words:
    res = []
    for word, _ in chapter2words[chapter].most_common(100):
        if not word in exclude:
            res.append(word)
    print(f'{chapter.strip():>34}', '\t'.join(res[:5]))

# join arcs
arc2words = defaultdict(Counter)
for chapter in chapter2words:
    if chapter.startswith('Interlude'):
        continue
    arc = chapter.split(' ')[0]
    arc2words[arc].update(chapter2words[chapter])

# >>> max([len(c) for c in arc2words])
# 13
exclude = set([word for word, _ in all.most_common(100)])
for chapter in arc2words:
    res = []
    for word, _ in arc2words[chapter].most_common(100):
        if not word in exclude:
            res.append(word)
    print(f'{chapter.strip():>14}', '\t:', '\t'.join(res[:5]))