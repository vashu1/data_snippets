import os
from collections import Counter, defaultdict
from PIL import Image

LINE_WIDTH = 7

rank = ['Dormant', 'Awakened', 'Fallen', 'Corrupted', 'Great', 'Cursed', 'Unholy']
hierarchy = ['Beast', 'Monster', 'Demon', 'Devil', 'Tyrant', 'Terror', 'Titan']
rainbow = [(255, 0, 0), (255, 127, 0), (255, 255, 0), (0, 255, 0), (0, 0, 255), (75, 0, 130), (148, 0, 211)]


def load(data, path, fname):
    with open(path + fname) as f:
        lines = f.readlines()
    c = Counter()
    for i, r in enumerate(rank):
        for j, h in enumerate(hierarchy):
            search = f'{r} {h}'.lower()
            val = sum([line.lower().count(search) for line in lines])
            if val:
                c[i*7 + j] = val
    n = int(fname.split('_')[1])
    if val:
        data[n] = val


data = defaultdict(Counter)
path = 'Shadow Slave/1/OEBPS/'  # load htmls
for fname in os.listdir(path):
    load(data, path, fname)
path = 'Shadow Slave/2/OEBPS/Text/'  # load xhtmls
for fname in os.listdir(path):
    load(data, path, fname)

max_chapter = max([ch_num for ch_num, _ in data.items()])
max_val = max([v for _, counter in data.items() for k, v in counter.most_common()])

img = Image.new('RGB', (7*7*LINE_WIDTH, max_chapter-1))
for y in range(max_chapter):
  for j in range(7*7):
      val = data[y][j]
      x = j*LINE_WIDTH
      img.paste(rainbow[j % 7] if val else (0,0,0),(x,y,x+LINE_WIDTH-1,y+1))

img.save("shadow_slave.png")