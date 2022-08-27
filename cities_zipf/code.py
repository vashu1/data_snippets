"""
$ wc -l *
   23469 cities15000.csv
   15494 worldcities.csv
 3173959 worldcitiespop.csv

lines = [line.strip() for line in open('cities15000.csv', encoding="ISO-8859-1").readlines()]
len([l for l in lines if ',RU,' in l])
1089


$ head worldcities.csv
"city","city_ascii","lat","lng","country","iso2","iso3","admin_name","capital","population","id"
"Tokyo","Tokyo","35.6850","139.7514","Japan","JP","JPN","Tōkyō","primary","35676000","1392685764"
"New York","New York","40.6943","-73.9249","United States","US","USA","New York","","19354922.0","1840034016"
...
$ cat worldcities.csv | grep \"RU\" | wc -l
     569


$ cat worldcitiespop.csv | awk -F, '{if (length($5)>0) print($5)}' | wc -l
   47981
...
cat worldcitiespop.csv | grep ^ru, | wc -l
...
$ cat worldcitiespop.csv | grep ^ru, | awk -F, '{if (length($5)>0) print($5)}' | wc -l
    4324
"""
import pycountry  # https://pypi.org/project/pycountry/
from collections import Counter, defaultdict
import csv
import scipy.optimize
import numpy as np
import math
import matplotlib.pyplot as plt

N_COUNTRIES = 30

"""
lines = [line.strip() for line in open('cities15000.csv', encoding="ISO-8859-1").readlines()]

#>>> lines[0]
#'geonameid,name,asciiname,alternatenames,latitude,longitude,feature class,feature code,country code,cc2,admin1 code,admin2 code,admin3 code,admin4 code,population,elevation,dem,timezone,modification date'
headers = list(enumerate(lines[0].split(',')))
lines = lines[1:]

countries = Counter()
for line in lines:
    c = line.split(',')[8]
    countries[c] += 1
"""
countries = Counter()
countries_populations = defaultdict(list)
c = 0
with open('cities15000.csv', encoding="ISO-8859-1") as csvfile:
    csvreaded = csv.reader(csvfile) # , delimiter=' ', quotechar='|'
    header = next(csvreaded)
    for row in csvreaded:
        if not row[14]:  # no population data
            continue
        c += 1
        try:
            country = row[8]
            population = int(row[14])
            countries[country] += 1
            countries_populations[country].append(population)
        except:
            print(len(row))
            print(row[5:])

capital_population = {}
capital_lattitude = {}
with open('worldcities.csv') as csvfile:
    csvreaded = csv.reader(csvfile) # , delimiter=' ', quotechar='|'
    header = next(csvreaded)
    for row in csvreaded:
        cc = row[5]
        if row[8] != 'primary':
            continue
        if not row[9] or not row[5]:
            print(f'{cc} {row[9]=} {row[5]=}')
            continue
        capital_population[cc] = int(float(row[9]))
        capital_lattitude[cc] = float(row[2])


# , (14, 'population')
for k in countries_populations:
    countries_populations[k].sort(reverse=True)

for k in countries_populations:
    if len(countries_populations[k]) < N_COUNTRIES:
        continue
    print(k, len(countries_populations[k]))


zipf = lambda n,v0,k: v0 / (n**k)
# https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.curve_fit.html
data = []
for c in countries_populations:
    if len(countries_populations[c]) < N_COUNTRIES:
        continue
    (v0, k), _ = scipy.optimize.curve_fit(zipf, list(range(1, N_COUNTRIES+1)),  countries_populations[c][:N_COUNTRIES],  p0=(countries_populations[c][0], 1))
    data.append((c, k))

data.sort(key=lambda v: v[1])
for c, k in data:
    cc = pycountry.countries.get(alpha_2=c).name
    print(cc, k)

data_dict = {c:k for c, k in data}

# https://www.kaggle.com/datasets/cityapiio/countries-population-2010-2020-data
# cat countries_general_info_historical.24-10-2021.csv | awk -F, '{if (NR>1) print $4,$5,$17;}' > countries_population.csv

country_population = {}
with open('countries_population.csv') as f:
    for line in f.readlines():
        c, _, p = line.strip().split(' ')
        country_population[c] = int(p)

def plot(*args, first_n = None):  # plt.xscale('log')  plt.loglog(x, y)
    plt.figure()
    for ps in args:
        # ps.sort(reverse=True)
        if first_n:
            ps = ps[:first_n]
        x = range(len(ps))
        y = list(reversed(sorted(ps)))
        plt.plot(x, y)
    plt.show()


"""
y = [2.56422, 3.77284, 3.52623, 3.51468, 3.02199]
x = [0.15, 0.3, 0.45, 0.6, 0.75]
n = [58, 651, 393, 203, 123]

plt.scatter(x, y)

for i, txt in enumerate(n):
    plt.annotate(txt, (x[i], y[i]))

plt.show()
"""

####### against population log10
def countries_plot(f):
    y = []
    x = []
    lbl = []
    for c in countries_populations:
        if len(countries_populations[c]) < N_COUNTRIES:
            continue
        if c not in country_population:
            print(f'{c=} not in countries_population')
            continue
        cc = pycountry.countries.get(alpha_2=c).name
        lbl.append(cc)
        x.append(data_dict[c])
        y.append(f(c))
    plt.scatter(x, y)
    for i, txt in enumerate(lbl):
        plt.annotate(txt, (x[i], y[i]))
    plt.show()

countries_plot(lambda c: math.log10(country_population[c]))
# latitude
countries_plot(lambda c: capital_lattitude[c])
# capital pop/countrypop
countries_plot(lambda c: capital_population[c] / country_population[c])
countries_plot(lambda c: math.log10(capital_population[c] / country_population[c]))

countries_plot(lambda c: countries_populations[c][0] / country_population[c])
countries_plot(lambda c: math.log10(countries_populations[c][0] / country_population[c]))

### GDP   https://www.kaggle.com/datasets/zackerym/gdp-annual-growth-for-each-country-1960-2020

gdp = {}
with open('GDP_annual_growth.csv') as csvfile:
    csvreaded = csv.reader(csvfile)
    header = next(csvreaded)
    for row in csvreaded:
        if row[2] != 'GDP (current US$)':
            continue
        ccc = row[1]
        try:
            cc = pycountry.countries.get(alpha_3=ccc).alpha_2  # name
            val = row[64]
            val = float(val if val else row[55])
            gdp[cc] = val
        except:
            print(f'who is {ccc}')

countries_plot(lambda c: math.log10(gdp.get(c, 1e8)))
countries_plot(lambda c: math.log10(gdp.get(c, 1e8)/ country_population[c]))

#TODO
"""
print loglog for all

try fit to cities 10:20
    change n and see where it fits

detect mix of 2 zipfs

world map color mark from red to green

Japan really that small?
china could be a little bigger
    https://en.wikipedia.org/wiki/King_effect
    French city sizes (where the point representing Paris is the "King", failing to conform to the stretched exponential[1]), and similarly for other countries with a primate city, such as the United Kingdom (London), and the extreme case of Bangkok (see list of cities in Thailand).
include countries with 10 too


A clustering method to construct cities from the bottom up by clustering populated areas obtained from high-resolution data finds a power-law distribution of city size consistent with Zipf's law in almost the entire range of sizes.[8] 
Rozenfeld, Hernán D., Diego Rybski, Xavier Gabaix, and Hernán A. Makse. 2011. "The Area and Population of Cities: New Insights from a Different Perspective on Cities." American Economic Review, 
ююю
In the study of the firms (business), the scholars do not agree that the foundation and the outcome of Gibrat's law are empirically correct.

"""

#### zipf mix test   - passwords split?
V01 = 1e6
V02 = 1e6 / 2
a1 = [int(V01/n) for n in range(1,20+1)]
a2 = [int(V02/(n**1.5)) for n in range(1,20+1)]
a3 = [int(V02/n) for n in range(1,10+1)]
a4 = [int(V02/(n**1.5)) for n in range(1,10+1)]

def plot_red_green(ys1, ys2):
    data = [(x, 1) for x in ys1] + [(x, 2) for x in ys2]
    data.sort(key=lambda v: v[0])
    data = [v[1] for v in data]
    plt.xscale('log')
    plt.yscale('log')
    plt.scatter([indx for indx, tp in enumerate(data) if tp == 1], ys1, color='red')
    plt.scatter([indx for indx, tp in enumerate(data) if tp == 2], ys2, color='blue')
    plt.show()


plt.scatter(range(1, len(a1)+1), a1, color='red')
plt.xscale('log')
plt.yscale('log')
plt.show()

plot_red_green(a1, a2)
plot_red_green(a1, a3)
plot_red_green(a1, a4)

###
def plot_country(cc):
    plt.xscale('log')
    plt.yscale('log')
    data = countries_populations[cc]
    if len(data) < 20:
        return
    plt.scatter(range(len(data)), data, color='red')
    plt.title(pycountry.countries.get(alpha_2=cc).name)
    plt.show()

for cc in countries_populations:
    plot_country(cc)

plot_country('KR')
plot_country('KP')

"Korea, Democratic People's Republic of", 'Korea, Republic of'

[(cc, pycountry.countries.get(alpha_2=cc).name) for cc in countries_populations if pycountry.countries.get(alpha_2=cc) and 'Korea' in pycountry.countries.get(alpha_2=cc).name]
"""
строить ломанную?

Azerbaijan
Bosnia
Bangladesh
Belarus   Under
Czechia

Germany break  Equador  Kenya  Kyrgystan

Georgia merge?   Cambodia  Libia  Puerto rico   Palestine  Uganda

Taiwan pieces

KNDR is different from Korea

wtf Mongolia

UK - to small biggest  Italy?
is china ok?   only head is slow?
"""

import matplotlib.pyplot as plt

V01 = 1e6
V02 = 1e6 / 2
a1 = [int(V01/n) for n in range(1,20+1)]
a2 = [int(V02/(n**1.5)) for n in range(1,20+1)]
a3 = [int(V02/n) for n in range(1,10+1)]

def plot_red_green(ys1, ys2):
    data = [(x, 1) for x in ys1] + [(x, 2) for x in ys2]
    data.sort(key=lambda v: v[0])
    data = [v[1] for v in data]
    plt.xscale('log')
    plt.yscale('log')
    plt.scatter([indx for indx, tp in enumerate(data) if tp == 1], ys1, color='red')
    plt.scatter([indx for indx, tp in enumerate(data) if tp == 2], ys2, color='blue')
    plt.show()

plot_red_green(a1, a2)
plot_red_green(a1, a3)


# Urbanization


code2_urbanization = {}

def get_val(row):
    for i in range(10):
        try:
            val = float(row[-2-i])
            return val
        except:
            pass
    return None

with open('urbanization_data_worldbank.csv') as csvfile:
    csvreaded = csv.reader(csvfile) # , delimiter=' ', quotechar='|'
    _ = next(csvreaded), next(csvreaded), next(csvreaded), next(csvreaded), next(csvreaded)
    for row in csvreaded:
        val = get_val(row)
        if val and pycountry.countries.get(alpha_3=row[1]):
            cc = pycountry.countries.get(alpha_3=row[1]).alpha_2
            code2_urbanization[cc] = get_val(row)

countries_plot(lambda c: code2_urbanization.get(c, 0))
