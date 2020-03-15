import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.gridspec import GridSpec as gs
import seaborn as sns

plt.style.use('seaborn')


# load data
asu = pd.read_csv('../../data/sites/asu_house.csv', converters={'Time':pd.to_datetime})
asu = asu[asu['CPM']=='Off'] # excluding cpm

open = asu[asu['LandDrain']=='Open']
closed = asu[asu['LandDrain']=='Closed']

indie = pd.read_csv('../../data/sites/indianapolis.csv', converters={'Time':pd.to_datetime})
indie = indie[indie['Side']=='Heated']


# pressure by season
fig, (ax1, ax2) = plt.subplots(1,2, sharey=True)

sns.boxplot(
    data=asu,
    x='Season',
    y='IndoorOutdoorPressure',
    #hue='LandDrain',
    ax=ax1,
)

sns.boxplot(
    data=indie,
    x='Season',
    y='IndoorOutdoorPressure',
    order=['Winter','Spring','Summer','Fall'],
    #hue='LandDrain',
    ax=ax2,
)

ax1.set(
    title='ASU house',
    ylim=[-5,5],
    ylabel='$p_{in} \\; \\mathrm{(Pa)}$'
)

ax2.set(
    title='EPA duplex',
    ylabel='',
)

fig.suptitle(
    'Distribution of indoor/outdoor pressure differences by season',
    y=0.95
)
plt.savefig('../../figures/transport_implications/seasonal_pressure.pdf', dpi=300)


# concentration by season
fig, (ax1, ax2) = plt.subplots(1,2, sharey=True)

sns.boxplot(
    data=asu,
    x='Season',
    y='logIndoorConcentration',
    hue='LandDrain',
    ax=ax1,
)

sns.boxplot(
    data=indie,
    x='Season',
    y='logIndoorConcentration',
    hue='Contaminant',
    order=['Winter','Summer','Fall'],
    #hue='LandDrain',
    ax=ax2,
)

ax1.set(
    title='ASU house',
    ylabel='$\\log_{10}{(c_{in})} \\; \\mathrm{(\\mu g/m^3)}$'
)

ax2.set(
    title='EPA duplex',
    ylabel='',
)

fig.suptitle(
    'Distribution of indoor contaminant concentrations by season',
    y=0.95
)
plt.savefig('../../figures/transport_implications/seasonal_concentration.pdf', dpi=300)


# air exchange rate ASU anaylsis
# concentration by season
fig, (ax1, ax2) = plt.subplots(1,2, )

sns.boxplot(
    data=closed,
    x='Season',
    y='AirExchangeRate',
    ax=ax1,
)

sns.boxplot(
    data=closed,
    x='Season',
    y='logAttenuationAvgGroundwater',
    ax=ax2,
)

ax1.set(
    title='Indoor contaminant concentration',
)

ax2.set(
    title='Air exchange rate',
    ylabel='$\\log_{10}{(c_{in})} \\; \\mathrm{(\\mu g/m^3)}$'
)

fig.suptitle(
    'asd by season',
    y=0.95
)

plt.show()
