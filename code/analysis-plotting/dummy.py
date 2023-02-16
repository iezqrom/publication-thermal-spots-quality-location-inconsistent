# %%
# import all_raw_aligned
import pandas as pd
from globals import path

all_raw_aligned = pd.read_csv(f"{path}/all_raw_aligned.csv")
# %%
# plot scatter plot with dummy data and star like shape
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.lines as mlines
from plotting import prettifySpinesTicks, removeSpines

# create dummy data
x = np.random.rand(100)
y = np.random.rand(100)
c = np.random.rand(100)

# create figure
fig, ax = plt.subplots(figsize=(10, 10))

# plot scatter plot
ax.scatter(x, y, c=c, s=100, marker="x")
# %%
# load pandas data
import pandas as pd

path = "/Users/ivan/Documents/aaa_online_stuff/coding/python/phd/expt17_spots/data/spot_unconfirmed.csv"

spot_unconfirmed = pd.read_csv(path)
# sum second column in spot_unconfirmed
spot_unconfirmed.iloc[:, 1].sum()
# %%
15 / (334 + 15)
# %%
