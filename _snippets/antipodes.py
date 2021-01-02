"""
Отсутствует объяснение явления антисимметрии в расположении материков и океанических впадин на поверхности
Земли (наличие океанического и материкового полушария Земли, Антарктический материк противостоит океанической впадине
Северного Ледовитого океана)

Криволуцкий А. Е. Голубая планета. Земля среди планет. Географический аспект. — М.: Мысль, 1985. — С. 228.

Антиподальное расположение материков и океанов
"""
from mpl_toolkits.basemap import Basemap
import math

sin  = lambda x: math.sin(math.radians(x))
cos  = lambda x: math.cos(math.radians(x))

bmap = Basemap(resolution='i')   # default: projection='cyl', resolution crude

grid = {}
total = total0 = 90*360
for lat in range(90):
    for lon in range(-180,180):
        total -= 1
        if total % 360 == 0: # print progress
            print(f'{round(total/total0*100,1)}%')
        anti_lat = -lat
        anti_lon = (lon+180+180)%360-180
        height = 4e4/360
        width = height * cos(lat)
        grid[(lon, lat)] = (bmap.is_land(*bmap(lon, lat)),bmap.is_land(*bmap(anti_lon, anti_lat)),width*height)

# earth surface /2  =  sum([grid[k][2] for k in grid]) = 256,863,666 - true is 255M km^2, close enough
# land surface = sum([grid[k][2] for k in grid if grid[k][0]]) + sum([grid[k][2] for k in grid if grid[k][1]])
# i resolution - 133.8M - true is 148 10% err is fine

# sum([grid[k][2] for k in grid if grid[k][0] != grid[k][1]])
# 122,189,662 or 47.5%

"""
a function that is much faster than basemap.is_land()
https://github.com/toddkarin/global-land-mask
It provides a global binary mask of land/ocean at 1 km resolution. 

The raw elevation data from the GLOBE dataset can be downloaded from https://www.ngdc.noaa.gov/mgg/topo/gltiles.html 
It is not necessary to download this data in order to use the global land mask. 
"""