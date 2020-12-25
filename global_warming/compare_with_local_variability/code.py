# see https://vashu11.livejournal.com/20302.html
import os
import functools
import operator
from datetime import datetime
from collections import defaultdict
import json
import matplotlib.pyplot as plt
import numpy as np

DATE_FILTER_PATTERN = ' 12:00"' # take noon data
CSVS_FOLDER = 'csvs'

os.system(f'unzip -o csvs.zip') # unpack zip

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

day_temperatures = [(el[0].year+el[0].timetuple().tm_yday/len(grouped_by_year[el[0].year]), el[2]) for el in data]
day_temperatures.sort(key = lambda v: v[0])
# yearly envelope
add_days = lambda year, lst: [(year+indx/len(lst), lst[indx])for indx in range(len(lst))]
envelope_min = [min(add_days(year, grouped_by_year[year]), key = lambda a:a[1]) for year in grouped_by_year]
envelope_max = [max(add_days(year, grouped_by_year[year]), key= lambda a: a[1]) for year in grouped_by_year]

year_temperatures = [(year+0.5, sum(temps)/len(temps)) for year, temps in grouped_by_year.items()]
year_temperatures.sort(key = lambda v: v[0])

# load anomalies from 'data.json'

years = grouped_by_year.keys()
YEARS = (min(years), max(years)+1)
world_temp_anomalies = json.load(open('data.json'))
world_temp_anomalies = [(float(year)+0.5, float(world_temp_anomalies['data'][str(year)])) for year in range(*YEARS)]
world_temp_anomalies.sort(key = lambda v: v[0])

def linear_regression(axis, color, xy_data,  digits = 3):
    m, b = np.polyfit(*zip(*xy_data), 1)  # m = slope, b = intercept
    axis.plot(YEARS, m * np.array(YEARS) + b, linestyle = '--', color=color, label=f'y = {round(m, digits)} * x {round(b,digits):+}')

# yearly temperatures
fig,ax = plt.subplots()
ax.plot(*zip(*year_temperatures), color="b")
ax.set_xlabel("year",fontsize=14)
ax.set_ylabel("Moscow",color="b",fontsize=14)
ax.set_ylim((7,10))
linear_regression(ax, 'b', year_temperatures)
ax.legend(loc=0)
ax2=ax.twinx()
ax2.plot(*zip(*world_temp_anomalies),color="r")
ax2.set_ylabel("World",color="r",fontsize=14)
ax2.set_ylim((0,3))
linear_regression(ax2, 'r', world_temp_anomalies)
ax2.legend(loc=3)
plt.savefig('year_variability.png',bbox_inches='tight')
plt.show()

# day temperatures
fig,ax = plt.subplots()
ax.plot(*zip(*day_temperatures), color="b")
ax.plot(*zip(*envelope_min), color="b", linestyle = ':')
ax.plot(*zip(*envelope_max), color="b", linestyle = ':')
ax.set_xlabel("day",fontsize=14)
ax.set_ylabel("Moscow",color="b",fontsize=14)
ax.set_ylim((-30,40))
ax.legend(loc=0)
ax2=ax.twinx()
ax2.plot(*zip(*world_temp_anomalies),color="r")
ax2.set_ylabel("World",color="r",fontsize=14)
ax2.set_ylim((-30,40))
ax2.legend(loc=3)
plt.savefig('day_variability.png',bbox_inches='tight')
plt.show()

# std per year
std_dev = [(year, np.array(temps).std()) for year, temps in grouped_by_year.items()]
plt.plot(*zip(*std_dev))
m, b = np.polyfit(*zip(*std_dev), 1) # m = slope, b = intercept
plt.plot(YEARS, m*np.array(YEARS) + b)
linear_regression(plt, 'r', std_dev)
plt.savefig('year_std.png',bbox_inches='tight')
plt.show()