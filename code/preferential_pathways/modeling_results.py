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
)

sns.lineplot(
    data=sim[(sim['Pathway']=='Yes') & (sim['Gravel']=='Yes') & (sim['Contaminated']=='Yes')],
    x='IndoorOutdoorPressure',
    y='logAttenuationGroundwater',
    ax=ax,
    color=colors[0],
)

# closed plots
sns.regplot(
    data=closed,
    x='IndoorOutdoorPressure',
    y='logAttenuationAvgGroundwater',
    x_bins=x_bins,
    fit_reg=False,
    ax=ax,
    color=colors[1],
)

sns.lineplot(
    data=sim[sim['Pathway']=='No'],
    x='IndoorOutdoorPressure',
    y='logAttenuationGroundwater',
    ax=ax,
    color=colors[1],
)


# cosmetic stuff

ax.set(
    title='Simulation prediction vs. ASU house field data considering preferential pathway status',
    ylabel='$\\log_{10}{(\\alpha_\\mathrm{gw})}$',
    xlabel='$p_\\mathrm{in} \\; \\mathrm{(Pa)}$'
)

handles, labels = [], []

handles.append(plt.Line2D((0,1),(0,1),color=colors[0]))
handles.append(plt.Line2D((0,1),(0,1),color=colors[1]))
handles.append(plt.Line2D((0,1),(0,1),color='k',marker='o',linestyle='None'))
handles.append(plt.Line2D((0,1),(0,1),color='k'))
labels.append('Preferential pathway open')
labels.append('Preferential pathway closed')
labels.append('Data')
labels.append('Prediction')

ax.legend(handles=handles,labels=labels)

plt.show()
