# download html here https://archiveofourown.org/works/11478249/chapters/25740126?view_adult=true
from collections import Counter
import re
from bs4 import BeautifulSoup

def html2txt(html):
    soup = BeautifulSoup(html, features="html.parser")
    # kill all script and style elements
    for script in soup(["script", "style"]):
        script.extract()    # rip it out
    # get text
    text = soup.get_text()
    # break into lines and remove leading and trailing space on each
    lines = (line.strip() for line in text.splitlines())
    # break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    # drop blank lines
    text = '\n'.join(chunk for chunk in chunks if chunk)
    return text

counter = Counter()
chapter_number = -1
words_count = 0
html = []
chapter2words = {}
words = [] #['f**k', 'F**k'] # count swears
for line in open('Worth the Candle.html').readlines():
    html.append(line)
    #for word in words:
    #    if word in line:
    #        words_count += len(re.findall(word, line))
    if '<h2' in line and '</h2>' in line:
        counter[chapter_number] = words_count
        words_count = 0
        chapter_number += 1
        text = html2txt(''.join(html)).lower()
        words = []
        for c in text:
            words.append(c if c.isalpha() else ' ')
        words = ''.join(words)
        words = Counter([word for word in words.split(' ') if word])
        chapter2words[chapter_number] = words
        html = []
        print(chapter_number)

del counter[-1]
del counter[0]
del counter[len(counter)]
#del chapter2words[-1]
del chapter2words[0]
del chapter2words[len(chapter2words)]

all = Counter()
for i in chapter2words:
    all += chapter2words[i]

all.most_common(1000)

exclude = set([word for word, _ in all.most_common(100)])
for i in range(1, len(counter)+1):
    #print(i, counter[i])
    res = []
    for word, _ in chapter2words[i].most_common(100):
        if not word in exclude:
            res.append(word)
    print(i, '\t'.join(res[:5]))