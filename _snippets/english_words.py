"""
English words with 4 double letters.
see comments https://archiveofourown.org/works/11478249/chapters/67836925#workskin
"""
import os

if not os.path.isfile('words.txt'):
    cmd = 'wget https://github.com/dwyl/english-words/raw/master/words.txt'
    res = os.system(cmd)
    if res:
        print(f'Couldn\'t run "{cmd}". Install wget and check Internet connection.')
        exit(1)

res = []
for line in open('words.txt').readlines():
    word = line.strip()
    line = list(word) # split to chars
    pairs = []
    for i in range(len(line)-1): # letter1, letter2 in zip(line[:-1], line[1:]):
        letter1 = line[i]
        letter2 = line[i+1]
        if letter1 == letter2:
            pairs.append(i)
    if len(pairs) > 3:
        print(word)
        # look for ajacent pairs
        #pairs2 = [(el - pairs[0]) for el in pairs]
        #if pairs2 == list(range(0,len(pairs2)*2, 2)):
        #    print(word)