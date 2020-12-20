import urllib2
from bs4 import BeautifulSoup

root = 'https://ru.wikipedia.org/'

def link_to_str(url):
    return urllib2.unquote(str(url))

def flatten(l):
    return [item for sublist in l for item in sublist]

def get_next_page_link(url):
    page = urllib2.urlopen(url)
    soup = BeautifulSoup(page, 'html.parser')
    el = soup.body.find(text='Следующая страница')
    if not el:
        return None
    return root + el.parent['href']

def get_pages(url):
    print '==== get_pages' 
    print 'Start page: ' + link_to_str(url)
    res = [url]
    while True:
        next_page = get_next_page_link(res[-1])
        if not next_page:
            return res
        print 'Next page: ' + link_to_str(next_page)
        res.append(next_page)

def get_page_links(url):
    page = urllib2.urlopen(url)
    soup = BeautifulSoup(page, 'html.parser')
    names = soup.find('div', attrs={'class': 'mw-category'})
    print 'get_page_links - ' + str(len(names.findAll('a')))
    return [root + x['href'] for x in names.findAll('a')]

def extract_date(page, txt, att):
    # import dateparser
    # dateparser.parse(u'13 января 2015 г.').strftime("%Y-%m-%d")
    try:
        p = soup.body.find(text=txt)
        return p.parent.parent.find('span', attrs={'class': att}).text
    except:
        return None

def get_birth_death(url):
    #print 'get_birth_death ' + link_to_str(url)
    page = urllib2.urlopen(url)
    soup = BeautifulSoup(page, 'html.parser')
    try:
        bdate = soup.find('span', attrs={'class': 'bday'}).text
    except:
        bdate = None
    try:
        ddate = soup.find('span', attrs={'class': 'dday'}).text
    except:
        ddate = None
    #print (bdate, ddate)
    return (bdate, ddate)

def process(url):
    pages = get_pages(url)
    links = flatten([get_page_links(x) for x in pages])
    return map(get_birth_death, links)

generals = [
'https://ru.wikipedia.org/wiki/%D0%9A%D0%B0%D1%82%D0%B5%D0%B3%D0%BE%D1%80%D0%B8%D1%8F:%D0%93%D0%B5%D0%BD%D0%B5%D1%80%D0%B0%D0%BB%D1%8B_%D0%B0%D1%80%D0%BC%D0%B8%D0%B8_(%D0%A1%D0%A1%D0%A1%D0%A0)',
'https://ru.wikipedia.org/wiki/%D0%9A%D0%B0%D1%82%D0%B5%D0%B3%D0%BE%D1%80%D0%B8%D1%8F:%D0%93%D0%B5%D0%BD%D0%B5%D1%80%D0%B0%D0%BB-%D0%BF%D0%BE%D0%BB%D0%BA%D0%BE%D0%B2%D0%BD%D0%B8%D0%BA%D0%B8_(%D0%A1%D0%A1%D0%A1%D0%A0)',
'https://ru.wikipedia.org/wiki/%D0%9A%D0%B0%D1%82%D0%B5%D0%B3%D0%BE%D1%80%D0%B8%D1%8F:%D0%93%D0%B5%D0%BD%D0%B5%D1%80%D0%B0%D0%BB-%D0%BB%D0%B5%D0%B9%D1%82%D0%B5%D0%BD%D0%B0%D0%BD%D1%82%D1%8B_(%D0%A1%D0%A1%D0%A1%D0%A0)',
'https://ru.wikipedia.org/wiki/%D0%9A%D0%B0%D1%82%D0%B5%D0%B3%D0%BE%D1%80%D0%B8%D1%8F:%D0%93%D0%B5%D0%BD%D0%B5%D1%80%D0%B0%D0%BB-%D0%BC%D0%B0%D0%B9%D0%BE%D1%80%D1%8B_(%D0%A1%D0%A1%D0%A1%D0%A0)'
]

a = map(process, generals)

import pickle
picklestring = pickle.dumps(a)
f = open('generals', 'w')
f.write(picklestring)
f.close()

gens = flatten(a)

gens = filter(lambda x: x[0] or x[1], gens)
>>> len(gens)
3513
>>> gens = [x[1] for x in gens]
>>> gens = filter(lambda x: x, gens)
>>> len(gens)
3196
>>> years = [x.split('-')[0] for x in gens]
>>> from collections import Counter
>>> for i in range(1940,1999):
...     print i, c[str(i)]

months = [x.split('-')[0]+'-'+x.split('-')[1] for x in gens if '-' in x]
>>> len(months)
2810
c = Counter()
for m in months:
    c[m] += 1
for i in range(1940,1999):
    for j in range(1,13):
        print str(i + (j-1)/float(12)), c[str(i)+'-'+str(j).zfill(2)]

for i in range(1940,1946):
    for j in range(1,13):
        print str(j).zfill(2) +'/'+ str(i-1900) , c[str(i)+'-'+str(j).zfill(2)]

for i in range(1945,1956):
    for j in range(1,13):
        print str(j).zfill(2) +'/'+ str(i-1900) , c[str(i)+'-'+str(j).zfill(2)]
