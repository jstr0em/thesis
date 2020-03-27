import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.gridspec import GridSpec as gs
import seaborn as sns

plt.style.use('seaborn')
colors = plt.rcParams['axes.prop_cycle'].by_key()['color']

# load data
data = pd.read_csv('../../data/sites/asu_house.csv')
open = data[data['LandDrain']=='Open']
closed = data[data['LandDrain']=='Closed']


nas = pd.read_csv('../../data/sites/north_island.csv')
nas.dropna(inplace=True)

print(nas)
