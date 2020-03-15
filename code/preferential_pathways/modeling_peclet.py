import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.gridspec import GridSpec as gs
import seaborn as sns

plt.style.use('seaborn')


sim = pd.read_csv('../../data/simulations/preferential_pathway.csv')
sim = sim[(sim['AirExchangeRate']==0.5) & (sim['IndoorOutdoorPressure'] <= 0)]

case1 = sim[(sim['Pathway']=='Yes') & (sim['Gravel']=='Yes') & (sim['Contaminated']=='Yes')]
case2 = sim[(sim['Pathway']=='Yes') & (sim['Gravel']=='No') & (sim['Contaminated']=='Yes')]
case3 = sim[(sim['Pathway']=='No')]


fig, ax = plt.subplots(dpi=300)

sns.lineplot(
    data=case1,
    x='IndoorOutdoorPressure',
    y='Peclet',
    ax=ax,
    label='Preferential pathway & gravel sub-base',
)

sns.lineplot(
    data=case2,
    x='IndoorOutdoorPressure',
    y='Peclet',
    ax=ax,
    label='Preferential pathway & no gravel sub-base',
)

sns.lineplot(
    data=case3,
    x='IndoorOutdoorPressure',
    y='Peclet',
    ax=ax,
    label='No preferential pathway & gravel sub-base',
)

ax.set(
    title='Péclet number as function of building pressurization for the different cases',
    yscale='log',
    xlabel='$p_\\mathrm{in} \\; \\mathrm{(Pa)}$',
    ylabel='Pe',
)

ax.legend()

plt.savefig('../../figures/preferential_pathways/modeling_result_peclet.pdf')
plt.show()
