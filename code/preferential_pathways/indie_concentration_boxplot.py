import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.gridspec import GridSpec as gs
import seaborn as sns

plt.style.use('seaborn')

data = pd.read_csv('../../data/sites/indianapolis.csv', converters={'Time':pd.to_datetime})
data = data[data['Side']=='Heated']


fig, ax = plt.subplots(dpi=300)


contaminants = data['Contaminant'].unique()

sns.boxplot(
    data=data,
    x='Contaminant',
    y='logIndoorConcentration',
    ax=ax,
)

ax.set(
    title='Distribution of contaminant concentrations at the EPA house duplex',
    ylabel='$\\log_{10}{(c_\\mathrm{in})} \\; \\mathrm{(\\mu g/m^3)}$',
)
plt.savefig('../../figures/preferential_pathways/indie_concentration_boxplot.pdf')

plt.show()
