__xkcd__ thinks that world IP map [looks like this](https://xkcd.com/195/).

Simply execute `./run.sh` to produce this true map of internet.

![Map of the Internet](https://dl.dropboxusercontent.com/s/18wo4fv25ri55k8/ip_world_map.png)

And TOP 10 and BOTTOM 10 countries:

#### TOP 10

coutry | count
--- |---
United States of America | 1574M
China | 357M
Japan | 196M
Germany | 133M
United Kingdom of Great Britain and Northern Ireland | 116M
Korea (Republic of) | 113M
Brazil | 89M
France | 82M
Canada | 71M
Italy | 56M

#### BOTTOM 10

coutry | count
--- |---
Montserrat | 2808
Niue | 2046
Norfolk Island | 2044
Saint Barthelemy | 2043
Korea (Democratic People's Republic of) | 1534
United States Minor Outlying Islands | 255
Pitcairn | 255
Antarctica | 255
Saint Helena, Ascension and Tristan Da Cunha | 255
South Georgia and The South Sandwich Islands | 255

## Notes:

Change `min_cidr_size` parameter in `code.py` for less detailed map.

IP2LOCATION-LITE-DB1.CSV not included - `run.sh` will try to download it.
