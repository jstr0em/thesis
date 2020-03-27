import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import pearsonr

plt.style.use('seaborn')
# reads data
df = pd.read_csv('../data/asu_house.csv', converters={'Time':pd.to_datetime})

# I drop the very low concentrations (<0.001) as these are way below MDL
# and just distorts the figure
df=df.dropna(subset=['IndoorConcentration'])[df['IndoorConcentration']>0.001]

# the distinction between the on and testing phases of CPM is not that relevant here
df['CPM'].replace(['Testing'],['On'],inplace=True)

fig, ax = plt.subplots(dpi=300)

for case in df['LandDrain'].unique():
    df_now = df[df['LandDrain']==case]
    r = pearsonr(df_now['IndoorOutdoorPressure'], df_now['logAttenuationAvgGroundwater'])

    sns.regplot(
        data=df_now,
        x='IndoorOutdoorPressure',
        y='logAttenuationAvgGroundwater',
        ax=ax,
        x_bins=np.linspace(-15,15,30),
        label=case+', r = %1.2f' % r[0],
    )

ax.set(
    title='Land drain\'s effect on VI pressure dependence at the ASU house\nPearson\'s r value for each case shown',
    ylabel='$\\log{(\\alpha)}$',
    xlabel='$p_\\mathrm{in/out} \; \\mathrm{(Pa)}$',
)
ax.legend(title='Land Drain')

plt.savefig('../figures/asu_pressure_dependence.pdf')
plt.savefig('../figures/asu_pressure_dependence.png')
plt.show()
