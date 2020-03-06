import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.gridspec import GridSpec as gs
import seaborn as sns

plt.style.use('seaborn')

data = pd.read_csv('../../data/sites/indianapolis.csv', converters={'Time':pd.to_datetime})
data = data[data['Side']=='Heated']



contaminants = data['Contaminant'].unique()

fig, ax = plt.subplots(dpi=300)

contaminants = data['Contaminant'].unique()

contaminant = contaminants[-1]
sns.lineplot(
    data=data[data['Contaminant']==contaminant],
    x='Time',
    y='logIndoorConcentration',
    ax=ax,
)

ax.set(
    title='%s concentration at the EPA house duplex' % contaminant.title(),
    ylabel='$\\log_{10}{(c_\\mathrm{in})} \\; \\mathrm{(\\mu g/m^3)}$',
)


plt.savefig('../../figures/preferential_pathway/indie_concentration_time_series.pdf')
plt.show()
