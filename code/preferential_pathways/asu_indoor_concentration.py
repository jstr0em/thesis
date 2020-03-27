import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

plt.style.use('seaborn')

# reads data
df = pd.read_csv('../data/asu_house.csv', converters={'Time':pd.to_datetime})

# I drop the very low concentrations (<0.001) as these are way below MDL
# and just distorts the figure
df=df.dropna(subset=['IndoorConcentration'])[df['IndoorConcentration']>0.001]

# the distinction between the on and testing phases of CPM is not that relevant here
df['CPM'].replace(['Testing'],['On'],inplace=True)

# setting up figure
fig, ax = plt.subplots(dpi=300)

# adding vertical line to indicate when the land drain was closed

# time point when land drain was closed
time_ld_closed = df[df['LandDrain']=='Closed']['Time'].min()

# mai
c_min = df['IndoorConcentration'].min()
c_max = df['IndoorConcentration'].max()

# draws the line
ax.plot(
    [time_ld_closed, time_ld_closed],
    [c_min, c_max],
    color='k',
)


# plots the indoor concentration over time
sns.lineplot(
    data=df,
    x='Time',
    y='IndoorConcentration',
    ax=ax,
    hue='CPM',
    hue_order=['Off', 'On'],
)

# cosmetic stuff
ax.set(
    yscale='log',
    ylabel='$c_\\mathrm{in} \\; \\mathrm{(\\mu g/m^3)}$',
    xlabel='Time (hr)',
    title='TCE concentration in the basement at the ASU house over time.\nVertical line indicates when the land drain was closed.'
)
plt.savefig('../figures/asu_indoor_concentration.pdf')
plt.savefig('../figures/asu_indoor_concentration.png')
plt.show()
