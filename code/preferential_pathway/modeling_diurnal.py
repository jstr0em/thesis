import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.gridspec import GridSpec as gs
import seaborn as sns
from scipy.interpolate import CubicSpline
from matplotlib.gridspec import GridSpec

plt.style.use('seaborn')


# load data
# asu house data
data = pd.read_csv('../../data/sites/asu_house.csv', converters={'Time':pd.to_datetime})
data = data[data['CPM']=='Off'] # excluding cpm
open_data = data[data['LandDrain']=='Open']
closed_data = data[data['LandDrain']=='Closed']

# simulation data
sim = pd.read_csv('../../data/simulations/diurnal.csv')

# sorting simulation data by cases
open = sim[(sim['ConstAe']=='No') & (sim['Pathway']=='Yes')]
open_const = sim[(sim['ConstAe']=='Yes') & (sim['Pathway']=='Yes')]
closed = sim[(sim['ConstAe']=='No') & (sim['Pathway']=='No')]
closed_const = sim[(sim['ConstAe']=='Yes') & (sim['Pathway']=='No')]

for df in (open_data, closed_data):
    r = df.resample('1D', on='Time', kind='timestamp')
    r = r['IndoorConcentration'].agg([np.mean, np.max, np.min, np.std])

    r['MaxDailyDelta'] = r['amax']/r['amin']
    r = r.replace([np.inf, -np.inf], np.nan).dropna()
    print(len(r) ,r['MaxDailyDelta'].median())



maxmin = lambda x: x['AttenuationGroundwater'].max()/x['AttenuationGroundwater'].min()

print( maxmin(open), maxmin(closed) )

colors = plt.rcParams['axes.prop_cycle'].by_key()['color']


#fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2,2,sharex=True,dpi=300)

fig = plt.figure(constrained_layout=True, dpi=300)

gs = GridSpec(3, 4, figure=fig)


ax1 = fig.add_subplot(gs[0, 0:2])
# identical to ax1 = plt.subplot(gs.new_subplotspec((0, 0), colspan=3))
ax2 = fig.add_subplot(gs[0, 2:4])
ax3 = fig.add_subplot(gs[1:3, 0:3])
ax4 = fig.add_subplot(gs[1:3, 3:4])


# pressure input
# needs some smoothing
x_smooth = np.linspace(0,23,200)
y_smooth = CubicSpline(open['Time'], open['IndoorOutdoorPressure'])(x_smooth)
ax1.plot(x_smooth, y_smooth, color='k')


# ae input
y_smooth = CubicSpline(open['Time'], open['AirExchangeRate'])(x_smooth)
ax2.plot(x_smooth, y_smooth, label='Diurnal $A_e$')

open_const.plot(
    x='Time',
    y='AirExchangeRate',
    ax=ax2,
    label='Constant $A_e$',
    legend=False,
)

# open cases
open.plot(
    x='Time',
    y='AttenuationGroundwater',
    ax=ax3,
    legend=False,
    color=colors[0],
    logy=True,
)
open_const.plot(
    x='Time',
    y='AttenuationGroundwater',
    ax=ax3,
    legend=False,
    color=colors[1],
    logy=True,
)


# closed cases
y_smooth = CubicSpline(closed['Time'], closed['AttenuationGroundwater'])(x_smooth)
ax3.semilogy(x_smooth, y_smooth, label='Diurnal $A_e$',linestyle='--',color=colors[0])
closed_const.plot(
    x='Time',
    y='AttenuationGroundwater',
    ax=ax3,
    linestyle='--',
    legend=False,
    color=colors[1],
    logy=True,
)


#formatting

ax1.set(
    title='Indoor/outdoor pressure difference input',
    ylabel='$p_\\mathrm{in} \\; \\mathrm{(Pa)}$',
)

ax2.set(
    title='Air exchange rate input',
    ylabel='$A_e \\; \\mathrm{(1/h)}$',
)

ax3.set(
    title='Predicted attenuation factor over a "typical" day',
    xlabel='Time (h)',
    ylabel='$\\alpha_\\mathrm{gw}$',
    #yscale='log',
    ylim=[5e-6, 2e-4]
)

ax4.axis('off')

# legend stuff
handles, labels = [], []

handles.append(plt.Line2D((0,1),(0,1),color=colors[0]))
handles.append(plt.Line2D((0,1),(0,1),color=colors[1]))
handles.append(plt.Line2D((0,1),(0,1),color='k'))
handles.append(plt.Line2D((0,1),(0,1),color='k',linestyle='--'))
labels.append('Varying air exchange rate')
labels.append('Constant air exchange rate')
labels.append('Preferential pathway present')
labels.append('Preferential pathway absent')


ax4.legend(handles, labels, loc='center')

plt.tight_layout()
plt.savefig('../../figures/preferential_pathway/modeling_diurnal.pdf')
#plt.show()
