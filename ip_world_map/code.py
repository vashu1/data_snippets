# see https://vashu11.livejournal.com/18365.html
from netaddr import *
import collections
import pandas as pd

# params
min_cidr_size = 256 * 256 * 4
GEO_FEED_FNAME = 'IP2LOCATION-LITE-DB1.CSV'

df = pd.read_csv(GEO_FEED_FNAME, names=['start','end','code','name'], header=None)
df = df.drop([0, 1]) # drop line: "0","16777215","-","-"

# convert intervals to cidrs and filter out small cidrs
filtered_cidrs = []
cnt = collections.Counter() # count ips per country
for _, row in df.iterrows():
    start, end, country_code, country_name = row
    cnt[country_name] += end - start
    if (end - start) < min_cidr_size: # preliminary filtering for speed
        continue
    # DB's (start, end) is not a valid CIDR, so we split it into CIDRs
    for cidr in iprange_to_cidrs(IPAddress(start), IPAddress(end)):
        if cidr.size >= min_cidr_size:
            filtered_cidrs.append((country_code, cidr))

del cnt['-'] # unknown country

# output result
with open('country_cidrs', 'w') as f:
    [f.write(f'{cidr}\t{country}\n') for country, cidr in filtered_cidrs]

print('TOP 10')
for country, count in cnt.most_common(10):
    print(f'{country}\t{round(count/1e6)}M')

print('BOTTOM 10')
for country, count in cnt.most_common()[-10:]:
    print(f'{country}\t{round(count)}')