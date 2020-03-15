import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.gridspec import GridSpec as gs
import seaborn as sns

plt.style.use('seaborn')


# load data
data = pd.read_csv('../../data/sites/asu_house.csv')
data = data[data['CPM']=='Off'] # excluding cpm

open = data[data['LandDrain']=='Open']
closed = data[data['LandDrain']=='Closed']


fig, (ax1,ax2) = plt.subplots(1,2,sharey=True, dpi=300)

for case, ax in zip( (open, closed), (ax1,ax2)):
    case_now = case[['AirExchangeRate', 'logAttenuationAvgGroundwater']].dropna()
    sns.kdeplot(
        data=case_now['AirExchangeRate'],
        data2=case_now['logAttenuationAvgGroundwater'],
        ax=ax,
        shade_lowest=False,
        shade=True,
    )

    ax.set(
        xlim=[0,1],
        ylim=[-7,-3.5],
        xlabel='$A_e \\; \\mathrm{(1/hr)}$',
    )

ax1.set(
    title='Preferential pathway open',
    ylabel='$ \\log_{10}{(\\alpha_\\mathrm{gw})}$',
)

ax2.set(
    title='Preferential pathway closed',
    ylabel='',
)


plt.savefig('../../figures/transport_implications/asu_its_application.pdf')
plt.show()
