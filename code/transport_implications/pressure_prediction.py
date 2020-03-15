import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from matplotlib.gridspec import GridSpec
from matplotlib.figure import figaspect

plt.style.use('seaborn')
def dP_T(dT):

    alpha = 0.040 # Pa/(m*K)
    dz = -3 # basement floor depth from surface m
    return alpha*dz*dT


def dP_T2(Ti, To, dz):
    alpha = 3454 # Pa*K/m
    return alpha*(1/Ti-1/To)*dz

def dP_wind(u, dir=None):
    Cj = 0.3 # surface pressure coefficient
    rho = 1 # air density kg/m^3
    sign = {
        'N': 1,
        'NE': 1,
        'E': 1,
        'SE': 1,
        'S': 1,
        'SW': 1,
        'W': -1,
        'NW': 1,
    }


    if dir is None:
        return 0.5*Cj*rho*u**2
    else:
        signs = []
        for dir_now in dir:
            signs.append(sign[dir_now])
        signs = np.array(signs)
        return 0.5*Cj*rho*-signs*u**2




df = pd.read_csv('../../data/sites/indianapolis.csv')
df = df.loc[df['Side']=='Heated']
df['Time'] = df['Time'].apply(pd.to_datetime)

def get_wind_direction(degree):
    degs = [0, 45, 90, 135, 180, 225, 270, 315, 360]
    dir = min(degs, key=lambda x:abs(x-degree))

    dirs = {
        '0': 'N',
        '45': 'NE',
        '90': 'E',
        '135': 'SE',
        '180': 'S',
        '225': 'SW',
        '270': 'W',
        '315': 'NW',
        '360': 'N',
    }

    return dirs[str(dir)]

df['Cardinal'] = df['WindDir'].apply(get_wind_direction)

df['dP_wind'] = dP_wind(df['WindSpeed'])

df['dP_wind_corr'] = dP_wind(df['WindSpeed'], df['Cardinal'].values)

df['dT'] = df['IndoorTemp'] - df['OutdoorTemp']

df['Ti'] = df['IndoorTemp']+273.15
df['To'] = df['OutdoorTemp']+273.15


df['dP_T'] = dP_T2(df['Ti'], df['To'], 3)

df['dP_T_wind'] = df['dP_T'] + df['dP_wind']
df['dP_T_wind_corr'] = df['dP_T'] + df['dP_wind_corr']
df['Time'] = df['Time'].apply(pd.to_datetime)

colors = plt.rcParams['axes.prop_cycle'].by_key()['color']

fig = plt.figure(figsize=(8, 10),dpi=300,)

gs = GridSpec(3,6, figure=fig)

# top row
ax1 = fig.add_subplot(gs[0,0:3])
ax2 = fig.add_subplot(gs[0,3:],sharex=ax1)
# bottom row
ax6 = fig.add_subplot(gs[2:,:],sharex=ax1)
# middle row
ax3 = fig.add_subplot(gs[1,0:2],sharex=ax1)
ax4 = fig.add_subplot(gs[1,2:4],sharex=ax1)
ax5 = fig.add_subplot(gs[1,4:],sharex=ax1)

fig.subplots_adjust(top=0.85)

# input data (temperature and wind speed)
df.plot( x='Time', y='dT', ax=ax1, color=colors[2], legend=False, )
df.plot( x='Time', y='WindSpeed', ax=ax2, legend=False, color=colors[3], sharex=ax1)

# cosmetic stuff
ax1.set(ylabel='$\\Delta T$ (C)', title='Indoor/outdoor temperature difference')
ax2.set(ylabel='u (m/s)',xlabel='', title='Wind speed')
ax2.tick_params(axis='x', labelbottom=False)

# middle row plots (individual dP contributions)
df.plot( x='Time', y='dP_T', ax=ax3, color=colors[1], legend=False)
df.plot( x='Time', y='dP_wind', ax=ax4, color=colors[1], legend=False)
df.plot( x='Time', y='dP_wind_corr', ax=ax5, color=colors[1], legend=False)

# cosmetic stuff

ax3.set(
    ylabel='$\\Delta p$ (Pa)',
    title='Temperature contribution',
    #ylim=[-3,1.5],
)


ax4.set(
    xlabel='',
    title='Wind contribution',
    #ylim=pressure_limits,
)

ax5.set(
    xlabel='',
    title='Direction corrected wind contr.',
    #ylim=pressure_limits,
)
 # N, NE, E, SE => negative
ax4.tick_params(axis='x', labelbottom=False)
ax5.tick_params(axis='x', labelbottom=False)

# comparing the actual and predicted values
df.plot( x='Time', y='IndoorOutdoorPressure', ax=ax6, )
df.plot( x='Time', y='dP_T_wind_corr', ax=ax6, alpha=0.8, )

# cosmetic stuff
ax6.set(
    ylabel='$\\Delta p$ (Pa)',
    title='Temperature + (corrected) wind contributions vs. recorded pressure difference',
    xlabel='Time',
)
ax6.legend(labels=['Recorded', 'Predicted'],frameon=True, loc='upper center')

fig.suptitle(
    'Predicted temperatue and wind induced indoor/outdoor pressure difference at the Indianapolis site',
    y=1.05
)

plt.tight_layout(h_pad=3)
plt.savefig('../../figures/transport_implications/pressure_prediction.pdf')


# boxplot comparison

fig, ax = plt.subplots()

sns.boxplot(
    data=df[['IndoorOutdoorPressure','dP_T', 'dP_T_wind', 'dP_T_wind_corr']],
    ax=ax,
)

print(df[['IndoorOutdoorPressure','dP_T', 'dP_T_wind', 'dP_T_wind_corr']].describe())

ax.set(
    title='Predicted temperature and wind contribution to building pressurization vs. recorded data at the EPA duplex',
    ylabel='$p_\\mathrm{in} \\; \\mathrm{(Pa)}$',
)

ax.set_xticklabels(['Recorded', 'Temp. contr.', 'Temp + wind', 'Temp. + dir. corr. wind'])
plt.tight_layout()
plt.savefig('../../figures/transport_implications/pressure_prediction_boxplot.pdf', dpi=300)

plt.show()
