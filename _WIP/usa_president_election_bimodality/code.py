# inspired by https://bash-m-ak.livejournal.com/91507.html

# Can't download
# 1840 - 1972 https://www.icpsr.umich.edu/web/ICPSR/studies/08611 https://doi.org/10.3886/ICPSR08611.v1
# 1900- http://oskicat.berkeley.edu/record=b23955097~S1

# 1976 - 2016 data https://electionlab.mit.edu/data
# 2020 data https://www.kaggle.com/unanimad/us-election-2020

# more https://www.icpsr.umich.edu/web/ICPSR/series/00059 https://libguides.princeton.edu/elections#s-lg-box-24284525

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random

def get_1976_2016():
	df = pd.read_csv('1976-2016-president.csv')
	df = df[df.party.isin(["democrat", "republican"])]
	df['percent'] = df['candidatevotes'] / df['totalvotes'] * 100
	return df[['year', 'state', 'party', 'percent']]

# TODO - check 2020 percents
def get_2000():
	df = pd.read_csv('archive/president_county_candidate.csv')
	biden = df[df.candidate == 'Joe Biden']   .groupby(['state']).sum().reset_index()
	trump = df[df.candidate == 'Donald Trump'].groupby(['state']).sum().reset_index()
	total = pd.read_csv('archive/president_state.csv') # 
	biden = pd.merge(biden, total,on='state')
	trump = pd.merge(trump, total,on='state')
	biden['party'] = 'democrat'
	trump['party'] = 'republican'
	df = pd.concat([biden, trump])
	df['year'] = 2020
	df['percent'] = df['total_votes_x'] / df['total_votes_y'] * 100
	return df[['year', 'state', 'party', 'percent']]

df = pd.concat([get_1976_2016(), get_2000()])
years = sorted(df.year.unique())

def get_year_data(df, year):
	df = df[(df.year == year)]
	democrat_data   = df[df.party == 'democrat']
	republican_data = df[df.party == 'republican']
	print(f'year {year} \tdem {democrat_data.shape[0]} \trep {republican_data.shape[0]}')
	data = [(democrat_data.query(f'state == "{state}"')['percent'].iloc[0], republican_data.query(f'state == "{state}"')['percent'].iloc[0]) \
	    for state in df.state.unique() if state in democrat_data['state'].values and state in republican_data['state'].values]
	data = data[:51]
	while len(data) < 51: # hack for single missing value
		data.append(random.choice(data))
	data.sort(key = lambda v: v[0] / v[1])
	return zip(*data)

fig, ax = plt.subplots()

#txt = fig.text(0.5,0.8, str(years[0]), fontsize=32)
dems, reps = get_year_data(df, years[0])
line1, = ax.plot(*zip(*enumerate(reps)))
line2, = ax.plot(*zip(*enumerate(dems)))

def init():  # only required for blitting to give a clean slate.
    line1.set_ydata([np.nan] * 51)
    line2.set_ydata([np.nan] * 51)
    return (line1, line2)


def animate(year):
    #plt.text(0.5, 1.01, str(year), horizontalalignment='center', verticalalignment='bottom', transform=ax.transAxes, fontsize=24) #set_text(str(year))
    plt.title(str(year))
    dems, reps = get_year_data(df, year)
    line1.set_ydata(dems)  # update the data.
    line2.set_ydata(reps)
    return (line1, line2)


ani = animation.FuncAnimation(
    fig, animate, frames = years, init_func=init, interval=500, blit=True, repeat = False)

# To save the animation, use e.g.
#
# ani.save("movie.mp4")
#
# or
#
# from matplotlib.animation import FFMpegWriter
# writer = FFMpegWriter(fps=15, metadata=dict(artist='Me'), bitrate=1800)
# ani.save("movie.mp4", writer=writer)

plt.show()


Dr. Mark Rowe


