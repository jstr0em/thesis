import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.gridspec import GridSpec as gs
import seaborn as sns
from scipy.stats import pearsonr


plt.style.use('seaborn')
colors = plt.rcParams['axes.prop_cycle'].by_key()['color']

# load data
data = pd.read_csv('../../data/sites/asu_house.csv')
data['CPM'].replace(['Testing'],['On'],inplace=True)

# & (data['CPM']=='Off')
data = data[(data['IndoorConcentration']>0.001) ] # removes points lower than detection limit

open = data[data['LandDrain']=='Open']
closed = data[data['LandDrain']=='Closed']

nas = pd.read_csv('../../data/sites/north_island.csv')

# KDE plot
fig, ax = plt.subplots(dpi=300)

dfs = [nas, open, closed]
alphas = [1, 0.8, 0.6]
labels = ['North Island', 'ASU house, land drain open', 'ASU house, land drain closed']

for df_now, alpha, label in zip(dfs, alphas, labels):
    df_now = df_now[['IndoorOutdoorPressure', 'logIndoorConcentration']].dropna()
    r = pearsonr(df_now['IndoorOutdoorPressure'], df_now['logIndoorConcentration'])
    df_now['logIndoorConcentration'] = df_now['logIndoorConcentration'] - df_now['logIndoorConcentration'].median()
    sns.kdeplot(
        data=df_now['IndoorOutdoorPressure'],
        data2=df_now['logIndoorConcentration'],
        ax=ax,
        alpha=alpha,
        shade_lowest=False,
        shade=True,
        label=label+', r = %1.2f' % r[0],
    )

ax.legend(loc='upper right',title='Site/dataset')

ax.set(
    xlim=[-30,15],
    ylim=[None,3],
    xlabel='$p_\\mathrm{in} \\; \\mathrm{(Pa)}$',
    ylabel='$\\log_{10}{(c_\\mathrm{in})} - \\mathrm{median}(\\log_{10}{(c_\\mathrm{in})})$',
    title='KDE plot associating indoor/outdoor pressure difference and\ndeviation from the median $\\log_{10}$ transformed indoor contaminant concentration'
)

plt.savefig('../../figures/preferential_pathways/indoor_pressure_kde.pdf')

fig, ax1 = plt.subplots(dpi=300)

nas.plot(
    x='Time',
    y='logIndoorConcentration',
    ax=ax1,
    grid=False,
    legend=False,
)

ax2 = ax1.twinx()
nas.plot(
    x='Time',
    y='IndoorOutdoorPressure',
    ax=ax2,
    grid=False,
    legend=False,
    color=colors[1],
    alpha=0.6,
)


ax1.set(
    title='Indoor contaminant concentration and indoor/outdoor pressure difference\nat the North Island NAS VI site',
    xlabel='Time (hr)',
    ylabel='$\\log_{10}{(c_\\mathrm{in})} \\; \\mathrm{(\\mu g/m^3)}$',

)

ax2.set(ylabel='$p_\\mathrm{in} \\; \\mathrm{(Pa)}$')
handles = []
handles.append(plt.Line2D((0,1),(0,1),color=colors[0]))
handles.append(plt.Line2D((0,1),(0,1),color=colors[1]))

ax1.legend(
    handles=handles,
    labels=['Indoor contaminant concentration', 'Indoor/outdoor pressure difference (right)']
    )

plt.savefig('../../figures/preferential_pathways/nas_indoor_conncentration_pressure.pdf')

plt.show()
