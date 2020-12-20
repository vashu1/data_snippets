# download mobi from https://github.com/Antigrapist/Mother_of_Learning then convert it to txt online
from collections import Counter

''' chapter header example
Chapter 002

Life's Little Problems
'''

def is_line_chapter(line):
    if not line.startswith('Chapter '):
        return False
    num = line[8:11]
    return len(num) == 3 and num[0].isdigit() and num[1].isdigit() and num[2].isdigit()


chapter_number = -1
text = []
chapter2words = {}
chapter_to_name = {}
lines = open('Mother of Learning - nobody103.txt').readlines()
for indx in range(len(lines)):
    line = lines[indx]
    text.append(line.strip())
    if is_line_chapter(line):
        chapter_number += 1
        chapter_to_name[chapter_number] = lines[indx+2].strip()
        text = ' '.join(text).lower()
        words = []
        for c in text:
            words.append(c if c.isalpha() else ' ')
        words = ''.join(words)
        words = Counter([word for word in words.split(' ') if word])
        chapter2words[chapter_number] = words
        text = []
        print(chapter_number)

del chapter2words[0]

all = Counter()
for i in chapter2words:
    all += chapter2words[i]

exclude = set([word for word, _ in all.most_common(100)])
for i in range(1, len(chapter2words)):
    res = []
    for word, _ in chapter2words[i].most_common(100):
        if not word in exclude:
            res.append(word)
    print(i, '\t'.join(res[:5]))