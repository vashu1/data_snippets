=====
get list of submitters -? kibana?   for last year?
get geo mapping

+ shor submitter count distribution
plot >500 <3000 separately
===
import re
from collections import Counter
import intervaltree
import ipaddress
import sys
import json
from iso3166 import countries
import geopandas
import pandas as pd
import math

feed_fname = 'geo_countries_ints.dsv'

def save(plt): # save plot
    fig = plt.get_figure()
    fig.savefig("output.png")

content = []
with open(feed_fname) as f:
    content = f.readlines()

content = [x.strip() for x in content] 

country_ip_tree = intervaltree.IntervalTree()
for line in content:
    s,e,c = line.split('|')[:3]
    s = int(s)
    e = int(e)
    country_ip_tree[s:(e+1)] = c

def get_ip_from_fname(fn):
    ip = None
    if fn.startswith('alerts.'):
        m = re.match('alerts.([0-9]*\.[0-9]*\.[0-9]*\.[0-9]*)[\.\-].*', fn)
        ip = m.group(1)
    else:
        if fn.startswith('arbor-stats.'):
            m = re.match('arbor-stats\.([0-9]*\.[0-9]*\.[0-9]*\.[0-9]*)[\.\-].*', fn)
            ip = m.group(1)
        else:
            if fn.startswith('arbor-stats-'):
                m = re.match('arbor-stats-[^\.]*\.([0-9]*\.[0-9]*\.[0-9]*\.[0-9]*)[\.\-].*', fn)
                ip = m.group(1)
    return ip

cnt_ip = Counter()
lines = open('2018_ls').readlines()
for line in lines:
    fpath = line.strip().split(' ')[-1]
    fname = fpath.split('/')[-1]
    cnt_ip[get_ip_from_fname(fname)] += 1

del cnt_ip[None]

cnt_country = Counter()
for ip in cnt_ip:
    if cnt_ip[ip] < 500: # cut off
        continue
    
    ip_int = int(ipaddress.IPv4Address(unicode(ip)))
    country = country_ip_tree[ip_int]
    if len(country) != 1:
        print('len(country) != 1 !!!!!!!!!!!!')
    
    country = list(country_ip_tree[ip_int])[0][2]
    cnt_country[country] += 1

world = geopandas.read_file(geopandas.datasets.get_path('naturalearth_lowres'))
cities = geopandas.read_file(geopandas.datasets.get_path('naturalearth_cities'))

counts = []
centers_x = []
centers_y = []
i=0 
for country in cnt_country:
    geoframe = world[world.iso_a3 == countries.get(country).alpha3]
    if geoframe[geoframe.continent == 'Europe'].empty or not geoframe[geoframe.name == 'Russia'].empty:
        continue
    if len(geoframe) == 0:
        print 'Skipping ', countries.get(country).name, '   Count = ', cnt_country[country]
        continue
    
    counts.append(cnt_country[country])
    x, y = geoframe.geometry.centroid.x, geoframe.geometry.centroid.y
    if country == 'US': # thank you, Alaska
        x += 15
        y -= 6
    if country == 'FR': # thank you, Corsica?
        x = float(cities[cities.name == 'Paris'].geometry.x) + 1
        y = float(cities[cities.name == 'Paris'].geometry.y) - 2
        print country, x, y
    centers_y.append(y)
    centers_x.append(x)

dfr = pd.DataFrame({'value': counts, 'x': centers_x, 'y': centers_y})
dfr['Coordinates'] = list(zip(dfr.x, dfr.y))
dfr['Coordinates'] = dfr['Coordinates'].apply(Point)
dfr['sz'] = dfr['value'].apply(math.sqrt)
gdf = geopandas.GeoDataFrame(dfr, geometry='Coordinates')

#world_plt = world.plot(color='white', edgecolor='black')
#a = gdf.plot(ax=world_plt, color='red', markersize=gdf['value'])   # SQRT ?????
#save(a)

a = world[world.name == 'France']
#a.geometry = a.geometry.intersection(shapely.geometry.polygon.Polygon([(0,0),(50,0),(50,80),(0,80)]))
a.pop_est = 4
world.drop(55)
world.append(a)

world.loc[55,'geometry'] = world.loc[55,'geometry'].intersection(shapely.geometry.polygon.Polygon([(0,0),(50,0),(50,80),(0,80)]))

world.loc[55,pop_est] 

#world[world.name == 'France'].geometry = [shapely.geometry.polygon.Polygon([(0,0),(50,0),(50,80),(0,80)])]

europe_plt = world[world.continent == 'Europe'][world.name != 'Russia'].plot(color='white', edgecolor='black')
a = gdf.plot(ax=europe_plt, color='red', markersize=gdf['value'])   # SQRT ?????
save(a)




df = pd.DataFrame(
    {'Country': [1,2,3,4,5],
     'Latitude': [-34.58, -15.78, -33.45, 4.60, 10.48],
     'Longitude': [-58.66, -47.91, -70.66, -74.08, -66.86]})

df['Coordinates'] = list(zip(df.Longitude, df.Latitude))
df['Coordinates'] = df['Coordinates'].apply(Point)
gdf = geopandas.GeoDataFrame(df, geometry='Coordinates')

for country in world:
    print country, type(country)
    break

# # We restrict to South America.  world[world.continent == 'South America'].plot(color='white', edgecolor='black')
plot1 = world.plot();
plot2 = plot1.plot(cities.plot(markersize=cities['values']))
fig = plot2.get_figure()
fig.savefig("output.png")

if True:
    plt.figure()
    plt.subplot(3, 1, 1)
    plt.plot(minutes, alt.degrees)
    plt.ylabel('elevation (deg)', fontsize=16)
    plt.ylim(0, 90)
    plt.xlim(35, 50)

    plt.subplot(3, 1, 2)
    plt.plot(minutes, az.degrees)
    plt.ylabel('azimuth (deg)', fontsize=16)
    plt.ylim(0, 360)
    plt.xlim(35, 50)

    plt.subplot(3, 1, 3)
    plt.plot(minutes, d.km)
    plt.ylabel('range (km)', fontsize=16)
    plt.xlabel('time after 05:00 (minutes)', fontsize=16)
    plt.ylim(250, 500)
    plt.xlim(35, 50)
    

cities.plot(markersize=cities['values'])

matplotlib.pyplot.text(x, y, s, fontdict=None, withdash=False, **kwargs)[source]

