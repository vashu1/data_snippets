# scrape articles from RAND site
import re
import requests
from bs4 import BeautifulSoup
import os

content = ['https://www.rand.org/pubs/papers.html'] + ['https://www.rand.org/pubs/papers.{}.html'.format(i) for i in range(2, 108)]

def get_articles(page):
    page = requests.get(page)
    soup = BeautifulSoup(page.content, 'html.parser')
    return [('https://www.rand.org' + link.get('href')) for link in soup.findAll('a', attrs={'href': re.compile("/pubs/papers/.*")})]

def get_pdfs(link):
    page = requests.get(link)
    soup = BeautifulSoup(page.content, 'html.parser')
    name = soup.findAll('h1', attrs={'id': 'RANDTitleHeadingId'})[0].text
    return set([(name, ('https://www.rand.org' if not 'http' in link.get('href') else '') + link.get('href')) for link in soup.findAll('a', attrs={'href': re.compile(".*\.pdf")})])

os.mkdir('pdfs')
for page in content[11:]:
    print('PAGE', page)
    articles = get_articles(page)
    for article in articles:
        print('ARTICLE', article)
        c = 0
        for d in get_pdfs(article):
            name, link = d
            if c > 0:
                name += '_{}'.format(c) 
            print('NAME', name)
            r = requests.get(link)
            l = len(r.content)
            print('LEN', l)
            with open('./pdfs/' + re.sub('[^\w\-_\. ]', '_', name) + '.pdf', 'wb') as f:
                f.write(r.content)
            c += 1
