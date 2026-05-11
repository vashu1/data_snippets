# pip install ebooklib
import random
import string
from ebooklib import epub
import ebooklib
import re
from bs4 import BeautifulSoup, NavigableString

TYPOS_PER_CHAPTER = 20

with open('dictionaries/words.txt') as f:
    WORDS = set([w.strip() for w in f.readlines()])

# Basic sentence matcher: sentence ending with . ! or ?
sentence_re = re.compile(r"[^.!?]+[.!?]")


def add_typo_(word):
    if not word: return word
    
    # Choose a random "error" type
    error_type = random.choice(['delete', 'swap', 'insert', 'replace'])
    idx = random.randint(0, len(word) - 1)
    
    if error_type == 'delete':
        return word[:idx] + word[idx+1:]
    
    elif error_type == 'swap' and len(word) > 1:
        idx = random.randint(0, len(word) - 2)
        chars = list(word)
        chars[idx], chars[idx+1] = chars[idx+1], chars[idx]
        return "".join(chars)
    
    elif error_type == 'insert':
        new_char = random.choice(string.ascii_lowercase)
        return word[:idx] + new_char + word[idx:]
    
    elif error_type == 'replace':
        new_char = random.choice(string.ascii_lowercase)
        return word[:idx] + new_char + word[idx+1:]
    
    return word


def add_typo(word):
    assert word in WORDS
    while True:
        r = add_typo_(word)
        if r not in WORDS:
            return r


def add_typo_to_html(html):
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
            candidates.append((text_node, match.start(), match.end(), sentence))

    replaced = False
    if candidates:
        text_node, start, end, old_sentence = random.choice(candidates)
        text = str(text_node)
        for ch in ['"', '!', '?', '.', ',', ':', ';', '-']:
            text = text.replace(ch, '')
        text = text.split(' ')
        word = random.choice(text)
        if word in WORDS:
            typo = add_typo(word)
            new_text = str(text_node).replace(word, typo)
            text_node.replace_with(new_text)
            replaced = True
            print('\n\n', text)
            print(word)
            print(typo)
            print(new_text)
    return replaced, str(soup)


path = '/Users/fullname/Downloads/FF11 Five Have a Wonderful Time.epub'
book = epub.read_epub(path)
ch = 0
for item in book.get_items_of_type(ebooklib.ITEM_DOCUMENT):
    print(f'\n\nCHAPTER {ch}')
    ch += 1
    html = item.get_content().decode("utf-8", errors="ignore")
    replace_cnt = 0
    total = 0
    while True:
        total += 1
        if total > TYPOS_PER_CHAPTER * 2:
            break  # lost case, empty chapter or something like that
        replaced, html = add_typo_to_html(html)
        if replaced:
            replace_cnt += 1
        if replace_cnt == TYPOS_PER_CHAPTER:
            break
    item.set_content(html.encode("utf-8"))

epub.write_epub(path.replace('.epub', '_typos.epub'), book)



