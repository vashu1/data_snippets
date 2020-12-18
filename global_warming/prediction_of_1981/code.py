from matplotlib.offsetbox import TextArea, DrawingArea, OffsetImage, AnnotationBbox

import matplotlib.pyplot as plt
import matplotlib.image as mpimg

import json

YEARS = (1950, 2020)
TEMPS = (-1.0+0.025,1.1+0.05)

world_temp_anomalies = json.load(open('data.json'))
"""
# test - we draw 4 peaks that touch axises of graph and axises of image to check fudge values
world_temp_anomalies['data']['1950'] = min(TEMPS)
world_temp_anomalies['data']['2010'] = max(TEMPS)
world_temp_anomalies['data']['1960'] = -0.3
world_temp_anomalies['data']['2020'] =  0.8
"""
years, world_temp_anomalies = zip(*[(year, float(world_temp_anomalies['data'][str(year)])) for year in range(*YEARS)])

# === DRAW

fig, ax = plt.subplots()

FIXED_YEARS = (YEARS[0]-10-0.5, YEARS[1]+3)
ax.set_xlim(*FIXED_YEARS)
ax.set_ylim(*TEMPS)

img = mpimg.imread('climate_1980.jpg')

imagebox = OffsetImage(img, zoom=0.3)
ab = AnnotationBbox(imagebox, (sum(FIXED_YEARS)/2, sum(TEMPS)/2))
ax.add_artist(ab)

plt.grid()

plt.plot(years, world_temp_anomalies, linewidth=1, zorder=10) # zorder to put it to foreground

plt.draw()
plt.savefig('climate_1980_and_modern.png',bbox_inches='tight')
plt.show()
