import os
import pandas as pd
import matplotlib.pyplot as plt
import math
from functools import reduce

os.system('wget http://oxrep.classics.ox.ac.uk/docs/StraussShipwrecks.zip')
os.system('unzip StraussShipwrecks.zip')

df = pd.read_excel('StraussShipwrecks.xlsx', engine='openpyxl')

df['mid_date'] = (df['Earliest date'] + df['Latest date'])/2
df = df.dropna(subset=['mid_date'])
df = df[-500 <= df['mid_date']]
df = df[df['mid_date'] <= 800]
df['century'] = df['mid_date'].apply(lambda year:math.ceil(year/100)*100)

all_wrecks = df.groupby('century')['Wreck ID'].count()

plt.figure()
all_wrecks.plot()
plt.savefig('all_wrecks.png',bbox_inches='tight')
plt.show()

# grouped by cargo

def get_groups_by_column(df, col):
    return df[df[col]].groupby('century')['Wreck ID'].count().to_frame(name=col)

"""
>>> df.columns
['Wreck ID', 'Strauss ID', 'Name', 'Parker Number', 'Sea area',
       'Country', 'Region', 'Latitude', 'Longitude', 'Min depth', 'Max depth',
       'Depth', 'Period', 'Dating', 'Earliest date', 'Latest date',
       'Date range', 'Mid point of date range', 'Probability',
       'Place of origin', 'Place of destination', 'Reference', 'Comments',
       'Amphorae', 'Marble', 'Columns etc', 'Sarcophagi', 'Blocks',
       'Marble type', 'Other cargo', 'Hull remains', 'Shipboard paraphernalia',
       'Ship equipment', 'Estimated tonnage', 'Amphora type']
"""

cargo_columns = ['Amphorae', 'Marble', 'Columns etc', 'Sarcophagi', 'Blocks',]

data = [get_groups_by_column(df, c) for c in cargo_columns]

table = reduce(lambda x, y: x.merge(y, how='outer', on='century'), data)
table = table.fillna(0)
table['non-amphorae'] = table.apply(lambda row: sum([row[c] for c in cargo_columns if c != 'Amphorae']), axis=1)

plt.figure()
table.plot()
plt.savefig('table.png',bbox_inches='tight')
plt.show()
