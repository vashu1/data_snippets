from matplotlib.backend_bases import MouseButton
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.colors as mcolors
from collections import deque, defaultdict
from geopy.distance import geodesic
from heapq import heappush, heappop  # -30% compared to deque
from datetime import datetime, timedelta
from collections import Counter, defaultdict
from matplotlib.animation import FuncAnimation, PillowWriter
import matplotlib.animation as animation

CENTER_DEGREES = 35, 48
SIZE_DEGREES = 2*10, 2*6

CENTER_DEGREES = 35, 49
SIZE_DEGREES = 2*6, 2*4

DATE_FORMAT = '%Y-%m-%d %H:%M'

xc, yc = CENTER_DEGREES
dx, dy = SIZE_DEGREES

def parse_date(str_dt, str_time):
    assert len(str_time) == 4
    str_time = f'{str_time[:2]}:{str_time[2:]}'
    return datetime.strptime(f'{str_dt} {str_time}', DATE_FORMAT)

def date_str(dt):
    return str(dt).split(' ')[0]


m = Basemap(projection='cyl', resolution='i')  # c (crude, the default), l (low), i (intermediate), h (high), f (full)
m.drawcoastlines()
m.drawmapboundary(fill_color='aqua')
_ = m.fillcontinents(color='white',lake_color='aqua')  #='coral'
m.drawcountries(linewidth=2)
m.drawrivers()
m.drawparallels(np.arange(-90.,120.,5.))
m.drawmeridians(np.arange(0.,420.,5.))
#m.drawmapboundary(fill_color='aqua')

ax = plt.gca()
ax.set_xlim(xc - dx//2, xc + dx//2)
ax.set_ylim(yc - dy//2, yc + dy//2)


"""
per country header
latitude,longitude,bright_ti4,scan,track,acq_date,acq_time,satellite,instrument,confidence,version,bright_ti5,frp,daynight,type

7 days header
latitude,longitude,bright_ti4,scan,track,acq_date,acq_time,satellite,confidence,version,bright_ti5,frp,daynight
44.99969,28.10388,296.54,0.52,0.5,2022-07-06,0048,N,nominal,2.0NRT,286.43,1.03,N
41.17414,32.63353,298.87,0.54,0.68,2022-07-06,0048,N,nominal,2.0NRT,287.28,1.25,N
41.26264,31.42544,304.21,0.47,0.64,2022-07-06,0048,N,nominal,2.0NRT,290.14,2.65,N

data format https://www.earthdata.nasa.gov/learn/find-data/near-real-time/firms/viirs-i-band-375-m-active-fire-data


Bright_ti4 	Brightness temperature I-4 	VIIRS I-4 channel brightness temperature of the fire pixel measured in Kelvin.
Bright_ti5 	Brightness temperature I-5 	I-5 Channel brightness temperature of the fire pixel measured in Kelvin.
DayNight 	Day or Night 	 D= Daytime fire, N= Nighttime fire

FRP 	Fire Radiative Power 	
FRP depicts the pixel-integrated fire radiative power in MW (megawatts). FRP depicts the pixel-integrated fire 
radiative power in MW (megawatts). Given the unique spatial and spectral resolution of the data, the VIIRS 375 m fire 
detection algorithm was customized and tuned in order to optimize its response over small fires while balancing the 
occurrence of false alarms. Frequent saturation of the mid-infrared I4 channel (3.55-3.93 µm) driving the detection of 
active fires requires additional tests and procedures to avoid pixel classification errors. As a result, sub-pixel fire 
characterization (e.g., fire radiative power [FRP] retrieval) is only viable across small and/or low-intensity fires. 
Systematic FRP retrievals are based on a hybrid approach combining 375 and 750 m data. In fact, starting in 2015 the algorithm 
incorporated additional VIIRS channel M13 (3.973-4.128 µm) 750 m data in both aggregated and unaggregated format.
"""

def load_data(fpath):
    per_day = Counter()
    points = defaultdict(list)
    with open(fpath) as f:
        for line in f.readlines()[1:]:
            line = line.strip().split(',')
            latitude, longitude, bright_ti4, scan, track, acq_date, acq_time, satellite, confidence, *_ = line
            latitude, longitude = float(latitude), float(longitude)
            if not ((xc - dx // 2) < longitude < (xc + dx // 2)):
                continue
            if not ((yc - dy // 2) < latitude < (yc + dy // 2)):
                continue
            # confidence 2635 hig 5020 low  54664 nominal
            #scan, track = float(scan), float(track)
            dt = parse_date(acq_date, acq_time)
            per_day[dt.date()] += 1
            points[date_str(dt.date())].append((longitude, latitude))
    return per_day, points

#acq_date, acq_time = '2022-07-06','0048'
data, points = load_data('data/fire_nrt_SV-C2_281946.csv')
#data2 = load_data('data/SUOMI_VIIRS_C2_Russia_Asia_7d.csv')

#data = data + data2
xs = list(sorted(set([k for k in data if k.year == 2022])))[46:]
ys = [data[dt] for dt in xs]
xs = [date_str(dt) for dt in xs]

def plot(*args, first_n = None):
    plt.figure()
    for ps in args:
        # ps.sort(reverse=True)
        if first_n:
            ps = ps[:first_n]
        x = range(len(ps))
        y = list(reversed(sorted(ps)))
        plt.plot(x, y)
    plt.show()




# weather

UKD_GHCND_CODE = 'UP'
stations_coords = {}
station_names = {}
with open('data/weather/ghcnd-stations.txt') as f:
    for line in f.readlines():
        if line.startswith(UKD_GHCND_CODE):
            code, lat, lon, _, name, *_ = line.split()
            lon, lat = float(lon), float(lat)
            if lon < 28:
                continue
            stations_coords[code] = (lon, lat)
            station_names[code] = name

weather = defaultdict(Counter)
with open('data/weather/2022.csv') as f:
    for line in f.readlines():
        code, dt, tag, val, *_ = line.split(',')
        if 'PRCP' == tag and code in stations_coords:
            weather[code][dt] += int(val)

for code in weather:
    print(station_names[code], len(weather[code]), weather[code].values())

#### plot
"""


#plt.figure()
fig, ax = plt.subplots()
plt.plot(xs, ys, 'r')
plt.plot(xs, [sum([weather[code][dt.replace('-', '')] for code in weather]) for dt in xs], 'b')
interval = 18
for i, label in enumerate(ax.get_xticklabels()):
    if i % interval != 0:
        label.set_visible(False)

plt.show()

"""

x,y = m(0, 0)
m_plot = m.plot(x, y, 'ro', markersize=3)[0]
m_plot.set_color('red')
m_plot2 = m.plot(x, y, 'ro', markersize=5)[0]
m_plot2.set_color('blue')
m_plot3 = m.plot(x, y, 'ro', markersize=5)[0]
m_plot3.set_color('gray')

def init():
    m_plot.set_data([], [])
    return m_plot,

# animation function.  This is called sequentially
def animate(i):
    dt = xs[i]
    print(dt)
    plt.title(dt)
    xxs = []
    yys = []
    for x, y in points[dt]:
        x, y = m(x, y)
        xxs.append(x)
        yys.append(y)
    m_plot.set_data(xxs, yys)
    # weather
    dtt = dt.replace('-', '')
    xw = [] ; yw = []
    xb = [] ; yb = []
    for code in weather:
        if dtt in weather[code]:
            x, y = stations_coords[code]
            if weather[code][dtt]:
                xb.append(x)
                yb.append(y)
            else:
                xw.append(x)
                yw.append(y)
    m_plot2.set_data(xb, yb)
    m_plot3.set_data(xw, yw)
    return m_plot, m_plot2, m_plot3

# call the animator.  blit=True means only re-draw the parts that have changed.
anim = animation.FuncAnimation(plt.gcf(), animate, init_func=init,
                               frames=len(xs), interval=500, repeat=False, blit=True)
# len(xs)
#plt.show()
anim.save("ukraine_fires_fps2.gif", dpi=300, writer=animation.PillowWriter(fps=2))

"""
TODO   rain >= 10 ?
"""