import pandas as pd
import json
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv('global-fossil-fuel-consumption.csv')
# >>> df.columns
# Index(['Year', 'Coal (TWh; direct energy)', 'Oil (TWh; direct energy)', 'Gas (TWh; direct energy)']
df.columns = ['year', 'coal', 'oil', 'gas']
df = df[df['year']>=1880]

""" see BP in Sources
    oil at 73,300 kg CO2 per TJ (3.07 tonnes per tonne of oil equivalent); 
    natural gas at 56,100 kg CO2 per TJ (2.35 tonnes per tonne of oil equivalent); 
    and coal at 94,600 kg CO2 per TJ (3.96 tonnes per tonne of oil equivalent
"""
def fuel_to_co2(row): # terawatt-hours -> tons of co2
    year, coal, oil, gas = row
    data = np.array([coal, oil, gas], dtype = np.float64)
    data[np.isnan(data)] = 0
    data *= 3600 # terawatt-hours -> TJ
    data *= [94.6, 73.3, 56.1]  # ton per TJ
    return [year, np.sum(data) + 5e9] # 5e9 - land use - see sources in readme

# axis{0 or ‘index’, 1 or ‘columns’},
df = df.apply(fuel_to_co2, axis='columns', result_type='expand')

years = df[0].to_numpy()
carbon = df[1].to_numpy()

world_temp_anomalies = json.load(open('data.json'))
temp = np.array([float(world_temp_anomalies['data'][str(int(year))]) for year in years])

# plot data
fig, ax2 = plt.subplots()

color = 'tab:blue'
ax2.set_ylabel('carbon', color=color)
ax2.plot(years, carbon, color=color)
ax2.tick_params(axis='y', labelcolor=color)
#plt. ylim(-1, 1)
#ax2.set_xlim([-1, 1])

ax2.plot(years-10, carbon,'--', color=color)
ax2.plot(years+10, carbon,'--', color=color)

#plt. ylim(-2e11, 1.4e12)

ax1 = ax2.twinx()  # instantiate a second axes that shares the same x-axis

color = 'tab:red'
ax1.set_xlabel('year')
ax1.set_ylabel('temperature anomaly', color=color)
ax1.plot(years, temp, color=color)
ax1.tick_params(axis='y', labelcolor=color)

#ax2.yaxis.limit_range_for_scale(0,1e12/2)
fig.tight_layout()  # otherwise the right y-label is slightly clipped
plt.savefig('temperature_anomaly_vs_carbon.png',bbox_inches='tight')
plt.show()