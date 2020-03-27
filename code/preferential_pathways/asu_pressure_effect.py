import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.gridspec import GridSpec

# reads data
df = pd.read_csv('../data/asu_house.csv', converters={'Time':pd.to_datetime})

# I drop the very low concentrations (<0.001) as these are way below MDL
# and just distorts the figure
df=df.dropna(subset=['IndoorConcentration','IndoorOutdoorPressure'])[df['IndoorConcentration']>0.001]

# the distinction between the on and testing phases of CPM is not that relevant here
df['CPM'].replace(['Testing'],['On'],inplace=True)

# remove CPM periods
df = df[df['CPM']=='Off']

# separate dataset into LD closed and open periods
ld_open = df[df['LandDrain']=='Open']
ld_closed = df[df['LandDrain']=='Closed']


# setting up figure
fig = plt.figure(dpi=300, constrained_layout=True)
gs = GridSpec(2,2, figure=fig)

ax1 = fig.add_subplot(gs[0,0])
ax2 = fig.add_subplot(gs[0,1], sharey=ax1,)
ax3 = fig.add_subplot(gs[1,0])
ax4 = fig.add_subplot(gs[1,1], sharex=ax3, sharey=ax3,)

ld_open.plot(
    x='Time',
    y=['IndoorConcentration','IndoorOutdoorPressure'],
    secondary_y='IndoorOutdoorPressure',
    ax=ax1,
    legend=False,
    alpha=0.8,
)

# here I remove the very extreme pressure as it really distorts the figure
ld_closed[ld_closed['IndoorOutdoorPressure']>-25].plot(
    x='Time',
    y=['IndoorConcentration','IndoorOutdoorPressure'],
    secondary_y='IndoorOutdoorPressure',
    ax=ax2,
    legend=True,
    alpha=0.8,
)



# land drain open KDE plot
sns.kdeplot(
    data=ld_open['IndoorOutdoorPressure'],
    data2=ld_open['logIndoorConcentration'],
    ax=ax3,
    shade=True,
    shade_lowest=False,
)

# land drain closed KDE plot
sns.kdeplot(
    data=ld_closed['IndoorOutdoorPressure'],
    data2=ld_closed['logIndoorConcentration'],
    ax=ax4,
    shade=True,
    shade_lowest=False,
)


# cosmetic stuff
ax1.set(
    title='Preferential pathway open',
    #xlim=[-5,5],
    yscale='log'
)

ax2.set(
    title='Preferential pathway open',
    #xlim=[-5,5],
    yscale='log'
)

ax3.set(
    title='Preferential pathway open',
    xlim=[-4,4],
)

ax4.set(
    title='Preferential pathway closed',
)

# legend
# TODO: Figure out some good way to display the legend. It seems like pandas makes a new
# axis for the secondary_y. You need to access this somehow to get handles etc. (or just make a custom legend)
plt.show()
