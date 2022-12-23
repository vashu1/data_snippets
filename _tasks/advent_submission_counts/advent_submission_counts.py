# export ADVENT_SESSION=_fill_
# Then run:
# python3 advent_submission_counts.py 2022 20

import requests
import sys
import os
from bs4 import BeautifulSoup
import time
import datetime

RESOLUTION = 60  # seconds

year = sys.argv[1]
day = sys.argv[2]

SESSION = os.environ['ADVENT_SESSION']


def get_stats():
    url = f'https://adventofcode.com/{year}/stats'
    response = requests.get(url, cookies={'session': SESSION})
    if response.status_code != 200:
        print(f'ERROR: {response.status_code=} {response.text=}')
        return None, None
    soup = BeautifulSoup(response.content, features='html.parser')
    row = soup.find('a', attrs={'href': f'/{year}/day/{day}'})
    if not row:  # not available yet
        return None, None
    both = int(row.find('span', attrs={'class': 'stats-both'}).text)
    only_fst = int(row.find('span', attrs={'class': 'stats-firstonly'}).text)
    return only_fst, both


seconds = datetime.datetime.now().second
time.sleep(60 - seconds)

next = time.time()
while True:
    fst, snd = get_stats()
    now = datetime.datetime.now()
    dt = now.strftime('%H:%M:%S')  # '%Y-%m-%d %H:%M:%S'
    delay = now.second  # strictly speaking eed to sub previous now
    print(f'{dt} {delay=} {fst=} {snd=}'.replace('=', ' '))
    #
    next += RESOLUTION
    time.sleep(next - time.time() - (delay if delay < 10 else 0))