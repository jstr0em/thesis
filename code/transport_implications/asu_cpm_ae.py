import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.gridspec import GridSpec as gs
import seaborn as sns

plt.style.use('seaborn')


# load data
data = pd.read_csv('../../data/sites/asu_house.csv')

data = data[data['CPM']!='Testing']

fig, ax = plt.subplots(dpi=300)

sns.boxplot(
    data=data,
    x='CPM',
    y='AirExchangeRate',
    ax=ax,
)

ax.set(
    title='Effect of CPM on the distribution of air exchange rate values at the ASU house',
    ylabel='$A_e \\; \\mathrm{(1/hr)}$',
)


plt.savefig('../../figures/transport_implications/asu_cpm_ae.pdf')

plt.show()
