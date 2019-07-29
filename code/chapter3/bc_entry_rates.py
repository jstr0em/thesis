import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

def j_ck(u, c):
    L = 15e-2 # slab thickness
    D = 7.4e-6 # diffusion constant
    Pe = u*L/D

    j = u*c/(1-np.exp(-Pe))
    return j


df = pd.read_csv('../../data/chapter3/bc_entry_rates.csv', header=4)
new_names = (
    'soil',
    'p',
    'p_not_used',
    'j_ghost',
    'c',
    'u',
)

df.rename(columns=dict(zip(list(df), new_names)), inplace=True)
df['j_expr'] = j_ck(df['u'], df['c'])

fig, (ax1, ax2) = plt.subplots(2,1,dpi=300,sharex=True)

sns.lineplot(data=df, x='p', y='j_ghost', hue='soil', ax=ax1)
sns.lineplot(data=df, x='p', y='j_expr', hue='soil', ax=ax2)

ax1.set_yscale('log')
ax2.set_yscale('log')
plt.show()
