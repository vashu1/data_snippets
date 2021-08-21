import os
import functools
import operator
from datetime import datetime
from collections import defaultdict
import random
import numpy as np

DATE_FILTER_PATTERN = ' 12:00"' # take noon data
CSVS_FOLDER = 'csvs'

# **csvs.zip** - [Moscow temperature data](https://rp5.ru/%D0%90%D1%80%D1%85%D0%B8%D0%B2_%D0%BF%D0%BE%D0%B3%D0%BE%D0%B4%D1%8B_%D0%B2_%D0%9C%D0%BE%D1%81%D0%BA%D0%B2%D0%B5_(%D0%92%D0%94%D0%9D%D0%A5\))
#os.system(f'unzip -o csvs.zip') # unpack zip

def load_csv(fname): # encoding is a mess, so it is faster to load it this way than tweak parser params
    with open(fname, encoding='cp1251') as f:
        data = f.readlines()
        data = [line for line in data if DATE_FILTER_PATTERN in line] # take noon data
        data = [line.replace(DATE_FILTER_PATTERN, '') for line in data] # drop time
        data = [line.replace('"', '').split(';')[:2] for line in data] # split into data and temperature
        parse_date = lambda s: datetime.strptime(s, '%d.%m.%Y')
        data = [(parse_date(dt), dt, float(temp)) for dt, temp in data] # convert types
        return data # list of tuples (date in datetime format, string date, temperature as float)

# load Moscow day temperatures and yearly averages

data = [load_csv(os.path.join(CSVS_FOLDER, fname)) for fname in os.listdir(CSVS_FOLDER)]
data = functools.reduce(operator.iconcat, data, []) # flatten

data.sort(key = lambda v: v[0]) # sort by date

grouped_by_year = defaultdict(list)
for dt, str_date, temp in data:
    grouped_by_year[dt.year].append(temp)

def avg(lst):
    return sum(lst) / len(lst)

def calc(s ,f):
    data1 = [f(t) for year in range(2006, 2006+7) for t in grouped_by_year[year]]
    data2 = [f(t) for year in range(2006 + 7, 2006 + 7*2) for t in grouped_by_year[year]]
    print(f'{s} {round(avg(data2) - avg(data1), 3)=}')

random.seed(1)
calc('avg', lambda t: t)
calc('rounded avg', lambda t: round(t))
real_thermometer = {t:(t + random.random()-0.5) for t in range(-100, 100)}
calc('random err', lambda t: real_thermometer[int(t)])

real_thermometer2 = {t:(t + np.random.normal(0, 1, 1)[0]) for t in range(-100, 100)}
calc('normal err', lambda t: real_thermometer2[int(t)])

calc('x^2 err', lambda t: int(t + t**2/500))
print([t**2/500 for t in range(-35, 35)])

