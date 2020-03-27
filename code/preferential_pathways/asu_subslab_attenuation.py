import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
plt.style.use('seaborn')

# reads data
df = pd.read_csv('../data/asu_house.csv', converters={'Time':pd.to_datetime})

# I drop the very low concentrations (<0.001) as these are way below MDL
# and just distorts the figure
df=df.dropna(subset=['IndoorConcentration'])[df['IndoorConcentration']>0.001]

# dropping CPM period because it is not relevant in this analysis here.
#df = df[df['CPM']=='Off']

# setting up figure
fig, ax = plt.subplots(dpi=300)


sns.boxplot(
    data=df,
    x='LandDrain',
    y='logAttenuationSubslab',
    hue='CPM',
    hue_order=['Off', 'On'],
    ax=ax,
)
# cosmetic stuff
ax.set(
    ylabel='$\\log_{10}(\\alpha_\\mathrm{subslab})$',
    xlabel='Land Drain Status',
    title='Distribution of TCE concentration in the basement,\nnormalized to the near-foundation contaminant concentration\nat the ASU house during different periods.'
)

plt.show()
