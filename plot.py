import numpy as np
import math
import time
import random
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection

grid_xdim = 100
grid_ydim = 100

x = np.linspace(-10, 10, grid_xdim)
y = np.linspace(-10, 10, grid_ydim)
x_grid, y_grid = np.meshgrid(x, y)


def plot_grid(x,y, ax=None, **kwargs):
    ax = ax or plt.gca()
    segs1 = np.stack((x,y), axis=2)
    segs2 = segs1.transpose(1,0,2)
    ax.add_collection(LineCollection(segs1, **kwargs))
    ax.add_collection(LineCollection(segs2, **kwargs))
    ax.autoscale()

fig, ax = plt.subplots()

plot_grid(x_grid,y_grid, ax=ax,  color="lightgrey")