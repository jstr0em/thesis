import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

def j_ck(u, c):
    L = 15e-2 # slab thickness
    D = 7.4e-6 # diffusion constant
    Pe = u*L/D

    j = u*c/(1-np.exp(-Pe))
    return j


#df = pd.read_csv('../../data/chapter3/bc_entry_rates.csv', header=4)

# TODO: Read u and c from the dataframe and use that to calculate j_ck, then compare with n from COMSOL
# p, u, c = df['p'], df['u'], df['c']

c = 0.01
u = np.logspace(-12,-2)


fig, (ax1, ax2) = plt.subplots()

# change u to p instead
ax1.loglog(u,j_ck(u,c), label='Flow into house')
ax1.loglog(u,j_ck(-u,c), label='Flow out of house')

ax1.set_title('Analytic flux expression')
ax1.set_ylim(bottom=1e-10)

fig, ax = plt.subplots(dpi=300)

ax.semilogy(p, j_ck(u, c), label='Flux expression')
ax.semilogy(p, n, label='Ghost cell flux')

ax2.set_title('Flux into ghost cell')

ax1.legend()
plt.show()
