# pip3 install num2words
from num2words import num2words

# If all the numbers from 1 to 1000 (one thousand) inclusive were written out in words, how many letters would be used?
# NOTE: Do not count spaces or hyphens.

def number_letters(n):
    s = num2words(n)
    s = s.replace(' ', '').replace('-', '')
    return len(s)

print(sum([number_letters(n) for n in range(1, 1000+1)]))
