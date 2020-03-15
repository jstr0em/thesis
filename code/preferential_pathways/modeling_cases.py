import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.gridspec import GridSpec as gs
import seaborn as sns

plt.style.use('seaborn')


# load data
data = pd.read_csv('../../data/sites/asu_house.csv')
open = data[data['LandDrain']=='Open']
closed = data[data['LandDrain']=='Closed']

sim = pd.read_csv('../../data/simulations/preferential_pathway.csv')
sim = sim[sim['AirExchangeRate']==0.5]
# minimum and maximum pressure
p_min, p_max = data['IndoorOutdoorPressure'].min(), data['IndoorOutdoorPressure'].max()
# number of bins to put data in
x_bins = np.arange(-5, 5, 0.5)

#fig, (ax1, ax2) = plt.subplots(2,1, dpi=300, sharey=True, sharex=True)
fig, ax = plt.subplots( dpi=300, sharey=True, sharex=True)
colors = plt.rcParams['axes.prop_cycle'].by_key()['color']


# open plots
sns.regplot(
    data=open,
    x='IndoorOutdoorPressure',
    y='logAttenuationAvgGroundwater',
    x_bins=x_bins,
    fit_reg=False,
    ax=ax,
    color=colors[0],
    label='Data'
)

sns.lineplot(
    data=sim[(sim['Pathway']=='Yes') & (sim['Gravel']=='Yes') & (sim['Contaminated']=='Yes')],
    x='IndoorOutdoorPressure',
    y='logAttenuationGroundwater',
    ax=ax,
    color=colors[0],
    label='Reference case'
)


sns.lineplot(
    data=sim[(sim['Pathway']=='Yes') & (sim['Gravel']=='Yes') & (sim['Contaminated']=='No')],
    x='IndoorOutdoorPressure',
    y='logAttenuationGroundwater',
    ax=ax,
    color=colors[1],
    label='Clean air in preferential pathway'
)

sns.lineplot(
    data=sim[(sim['Pathway']=='Yes') & (sim['Gravel']=='No') & (sim['Contaminated']=='Yes')],
    x='IndoorOutdoorPressure',
    y='logAttenuationGroundwater',
    ax=ax,
    color=colors[2],
    label='No gravel sub-base'
)


# cosmetic stuff

ax.set(
    title='Predicted effect of removing gravel sub-base and contaminant vapors from\npreferential pathway vs. original/reference prediction and data',
    ylabel='$\\log_{10}{(\\alpha_\\mathrm{gw})}$',
    xlabel='$p_\\mathrm{in} \\; \\mathrm{(Pa)}$'
)

ax.legend()
plt.show()
