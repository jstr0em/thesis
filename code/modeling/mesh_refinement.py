import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.gridspec import GridSpec as gs
import seaborn as sns

plt.style.use('seaborn')

df = pd.read_csv('../../data/simulations/mesh_refinement.csv', header=4)

dalpha = [np.nan]
alphas = df['alpha (1)'].values
for i  in range(len(alphas)-1):
    dalpha.append(np.abs(alphas[i+1]-alphas[i])/alphas[i])




df['dalpha'] = np.array(dalpha)
print(df)
fig, ax = plt.subplots()


df.plot(
    y=['dalpha'],
    ax=ax,
    logy=True,
    legend=False,
)

ax.set(
    xlabel='Mesh refinement iteration',
    ylabel='$\\frac{c_\\mathrm{in,i+1}-c_\\mathrm{in,i}}{c_\\mathrm{in,i}}$',
    title='Relative error of indoor contaminant concentration for each mesh refinement iteration',
)

plt.savefig('../../figures/methods/mesh_refinement_error.pdf', dpi=300)
plt.show()
