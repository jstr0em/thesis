import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import pearsonr

plt.style.use('seaborn')
# reads data
df = pd.read_csv('../data/indianapolis.csv', converters={'Time':pd.to_datetime})

#df = df[df['Contaminant']=='Trichloroethene']

# I drop the very low concentrations (<0.001) as these are way below MDL
# and just distorts the figure
#df=df.dropna(subset=['IndoorConcentration'])[df['IndoorConcentration']>0.001]

# the distinction between the on and testing phases of CPM is not that relevant here
#df['CPM'].replace(['Testing'],['On'],inplace=True)

fig, ax = plt.subplots(dpi=300)

contaminants = df['Contaminant'].unique()

for contaminant in contaminants:
    df_now = df[df['Contaminant']==contaminant].dropna()
    r = pearsonr(df_now['IndoorOutdoorPressure'], df_now['logIndoorConcentration'])
    sns.regplot(
        data=df_now,
        x='IndoorOutdoorPressure',
        y='logIndoorConcentration',
        ax=ax,
        x_bins=np.linspace(-15,15,30),
        label=contaminant.title()+', r = %1.2f' % r[0],
    )

ax.set(
    title='Indoor contaminant concentration vs. indoor/outdoor pressure difference at the Indianapolis site\nPearson\'s r value for each contaminant shown',
    ylabel='$\\log{(c_\\mathrm{in})} \\; \\mathrm{\\mu g/m^3}$',
    xlabel='$p_\\mathrm{in/out} \; \\mathrm{(Pa)}$',
)


ax.legend(title='Contaminant',frameon=True)

#plt.savefig('../figures/asu_pressure_dependence.pdf')
#plt.savefig('../figures/asu_pressure_dependence.png')
plt.show()
