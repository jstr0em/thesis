import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.gridspec import GridSpec as gs
import seaborn as sns

plt.style.use('seaborn')

# laods data
sim = pd.read_csv('../../data/simulations/peclet_soil_types_depth_pressure.csv', header=4)

sim = sim[sim['p_in (Pa)'] == -15] # picks only largest depressurization

# renames columns
sim.rename(
    columns={
        '% matsw.comp1.sw1': 'Soil Type',
        'Pe (1)': 'Pe',
        'depth (m)': 'Foundation type',
    },
    inplace=True,
)

# renames foundation types by name instead of depth
sim['Foundation type'].replace(
    to_replace={
        1: 'Basement',
        0.15: 'Slab-on-grade',
    },
    inplace=True,
)

# renames soil index to their respective names
sim['Soil Type'].replace(
    to_replace={
        1: 'Sandy Loam',
        2: 'Sand',
        3: 'Loamy Sand',
        4: 'Sandy Clay Loam',
        5: 'Loam',
        6: 'Silt Loam',
        7: 'Clay Loam',
        8: 'Silty Clay Loam',
        9: 'Silty Clay',
        10: 'Silt',
        11: 'Sandy Clay',
        12: 'Clay',
    },
    inplace=True,
)

sim.sort_values(by='Pe', inplace=True, ignore_index=True)

fig, ax = plt.subplots(dpi=300)

print(sim['Soil Type'].unique())

ax.plot(
    sim['Soil Type'].unique(),
    np.repeat(1, len(sim['Soil Type'].unique())),
    color='k',
    linestyle='--'
)

sns.lineplot(
    data=sim,
    x='Soil Type',
    y='Pe',
    ax=ax,
    hue='Foundation type',
    sort=False,
    legend=False,
    marker='o',
)

ax.set(
    title='Peclet number for contaminant transport through foundation crack\nBuilding depressurized at -15 Pa',
    yscale='log',
)

plt.xticks(rotation=45)

# custom legend
ax.legend(
    title='Foundation type',
    labels=['Advective threshold','Basement', 'Slab-on-grade'],
)


plt.tight_layout()

plt.savefig('../../figures/transport_implications/peclet_cases.pdf')
plt.show()
