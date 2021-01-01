import os
import pandas as pd
import matplotlib.pyplot as plt
import math
from functools import reduce
from mpl_toolkits.basemap import Basemap

# get dataset
if not os.path.exists('StraussShipwrecks.zip'):
    os.system('wget http://oxrep.classics.ox.ac.uk/docs/StraussShipwrecks.zip')
    os.system('unzip StraussShipwrecks.zip')

df = pd.read_excel('StraussShipwrecks.xlsx', engine='openpyxl')

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

# plot all shipwrecks
df['mid_date'] = (df['Earliest date'] + df['Latest date'])/2
df = df.dropna(subset=['mid_date'])
df = df[-500 <= df['mid_date']]
df = df[df['mid_date'] <= 800]
df['century'] = df['mid_date'].apply(lambda year:math.ceil(year/100)*100)

all_wrecks = df.groupby('century')['Wreck ID'].count()

all_wrecks.plot()
plt.savefig('all_wrecks.png',bbox_inches='tight')
plt.show()

# grouped by cargo

def get_groups_by_column(df, col):
    return df[df[col]].groupby('century')['Wreck ID'].count().to_frame(name=col)

cargo_columns = ['Amphorae', 'Marble', 'Columns etc', 'Sarcophagi', 'Blocks',]

data = [get_groups_by_column(df, c) for c in cargo_columns]
table = reduce(lambda x, y: x.merge(y, how='outer', on='century'), data)

df['non-amphorae'] = df.apply(lambda row: any([row[c]==True for c in cargo_columns if c != 'Amphorae']), axis=1)
non_amphorae = get_groups_by_column(df, 'non-amphorae')
table = table.merge(non_amphorae, how='outer', on='century')

table = table.fillna(0)

table.plot()
plt.savefig('table.png',bbox_inches='tight')
plt.show()

# draw coordinates on map

# df['Longitude'].value_counts()  Length: 269

fig, axs = plt.subplots(1, 1, figsize=(10,10))
x1 = -10 # Mediterranean Sea
x2 = 37
y1 = 30
y2 = 46

# resolution = c (crude), l (low), i (intermediate), h (high), f (full) or None.
# projection = list(mpl_toolkits.basemap.projection_params.keys())
bmap = Basemap(resolution='i', projection='merc', llcrnrlat=y1, urcrnrlat=y2, llcrnrlon=x1, urcrnrlon=x2)
bmap.drawcoastlines(linewidth=0.5) # m.drawcountries(linewidth=0.5)

# fig.clear()
for index, row in df.iterrows():
    lo, la = row['Longitude'], row['Latitude']
    if not (lo > 0 and la > 0):
        continue
    c = 'green' if row['mid_date'] < 200 else 'red'
    _ = plt.plot(*bmap(lo, la), 'ok', color=c, markersize=1)

plt.tight_layout()
plt.savefig('map.png', dpi=300, bbox_inches='tight')
plt.show()
