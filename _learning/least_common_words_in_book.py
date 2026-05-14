# pip install ebooklib
import random
import string
from ebooklib import epub
import ebooklib
import re
from bs4 import BeautifulSoup, NavigableString

LEAST_USED_CNT = 300

# Basic sentence matcher: sentence ending with . ! or ?
sentence_re = re.compile(r"[^.!?]+[.!?]")

freq_lst = open('dictionaries/unigram_freq.csv').readlines()
freq_lst = [i.strip() for i in freq_lst][1:]
freq_lst = {i.split(',')[0]:i.split(',')[1] for i in freq_lst}


def filter_alphabet_symbols(word):
    return ''.join([ch for ch in list(word) if ch.isalpha()])


usage = {}
words = {}
path = '/Users/fullname/Downloads/FF11 Five Have a Wonderful Time.epub'
book = epub.read_epub(path)
ch = 0
for item in book.get_items_of_type(ebooklib.ITEM_DOCUMENT):
    html = item.get_content().decode("utf-8", errors="ignore")
    soup = BeautifulSoup(html, "html.parser")
    candidates = []
    for text_node in soup.find_all(string=True):
        if not isinstance(text_node, NavigableString):
            continue
        if text_node.parent.name in {"script", "style"}:
            continue
        text = str(text_node)
        for match in sentence_re.finditer(text):
            sentence = match.group()
            text = sentence.split(' ')
            text = [filter_alphabet_symbols(w) for w in text]
            text = [w.lower() for w in text if w]
            for w in text:
                if w in freq_lst:
                    words[w] = freq_lst[w]
                    usage[w] = sentence


words = [(k, int(v)) for k, v in words.items()]
words.sort(key=lambda v: v[1])

for n, (w, _) in enumerate(words[:LEAST_USED_CNT]):
    print(n + 1, w, ':', usage[w])
