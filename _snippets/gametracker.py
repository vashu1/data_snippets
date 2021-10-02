from bs4 import BeautifulSoup
import requests

PAGE_COUNT = 1049 # see https://www.gametracker.com/search/?searchipp=50&searchpge=2#search
url_root = 'https://www.gametracker.com/'
url_list = [url_root + url for url in ['search/?searchipp=50#search'] + ['search/?searchipp=50&searchpge={}#search'.format(page) for page in range(2, PAGE_COUNT + 1)]]

def get_page(url, f):
    print('get_page', url)
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content)
    table = soup.find('table', attrs={'class': 'table_lst'})
    rows = table.findChildren("tr" , recursive=False)
    rows = rows[1:-1] # drop header
    for row in rows:
        vals = row.findChildren("td" , recursive=False)
        game = '#'.join([img['alt'].strip().replace(' ', '_') for img in vals[1].find_all('img', alt=True)])
        ip_port = vals[6].text.strip().replace(' ', '_')
        #print(game, ip_port)
        f.write(game + ' ' + ip_port + '\n')

f = open('games', 'w')
for url in url_list:
    get_page(url, f)

f.close()
