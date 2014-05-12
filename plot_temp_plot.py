from __future__ import print_function, division

import glob
import re
import pandas as pd
import numpy as np
import matplotlib as mpl

from matplotlib import pyplot as plt
from itertools import starmap
from collections import OrderedDict
from operator import itemgetter, add
from functools import partial

month_names = [
    'January', 'February', 'March', 
    'April', 'May', 'June','July',
    'August','September', 'October',
    'November', 'December'
]

prefix_conf = {
    'tmin': {
        'imshow': {'cmap': mpl.cm.spectral, 'vmin': -15, 'vmax': 40},
        'coefficient': 1/10,
    },
    'tmax': {
        'imshow': {'cmap': mpl.cm.spectral, 'vmin': -15, 'vmax': 40},
        'coefficient': 1/10,
    },
    'prec': {
        'imshow': {'cmap': mpl.cm.Paired, 'vmin': 0, 'vmax': 550},
        'coefficient': 1,
    },
}

def read_plot(prefix, ax):
    files = glob.glob('/media/lagring/worldclim/mip_16/{}*.npz'.format(prefix))
    files.sort(key=lambda x: int(re.findall('_[0-9]*_',x)[0].replace('_','')))
    for f in files: print(f)
    datas = map(
        lambda f: np.load(f)['arr_0'] * prefix_conf[prefix]['coefficient'],
        files,
    )
    def linear(d0, d1, n=2):
        return [(d1 - d0) * x/n + d0 for x in range(n)]
    N = len(datas)
    datas = reduce(
        add,    
        [linear(datas[n%N], datas[(n+1)%N]) for n in range(N)]
    )
    month_plots = map(
        partial(ax.imshow, **prefix_conf[prefix]['imshow']),
        datas,
    )
    map(
        lambda im: im.set_visible(False),
        month_plots[1:],
    )
    return datas, month_plots

fig = plt.figure()
ax1 = fig.add_subplot(2, 2, 1)
ax2 = fig.add_subplot(2, 2, 2, sharex=ax1, sharey=ax1)
ax3 = fig.add_subplot(2, 2, 3, sharex=ax1, sharey=ax1)
ax4 = fig.add_subplot(2, 2, 4)
#ax42 = ax4.twinx()
axs = [ax1, ax2, ax3]
plt.hold(True)
data, min_max_plots = zip(*list(starmap(
    read_plot,
    zip(('tmin', 'tmax', 'prec'), axs),
)))
month_plots = zip(*min_max_plots)
set_visible_false = lambda x: x.set_visible(False)
set_visible_true = lambda x: x.set_visible(True)
map(
    lambda x: map(set_visible_false, [x.axes.xaxis, x.axes.yaxis]),
    axs,
)
plt.subplots_adjust(0.02,0.06, 0.98, 0.98, 0.01, 0.01)
current = 0
map(lambda ax: ax.set_title(str(current)), axs)
lines = []
def plot_graphs(x, y, ax):
    global lines
    map(set_visible_true, lines)
    col = mpl.colors.cnames.keys()[len(lines)]
    ax.set_title(str(len(lines)) + str(col))
    plt.pause(0.03)
    lines += ax.plot(
        map(itemgetter((y, x)), data[0]),
        color=col
    )
    plt.pause(0.03)
    lines += ax.plot(
        map(itemgetter((y, x)), data[1]),
        color=col
    )
    plt.pause(0.03)
#     lines += ax42.plot(
#         map(itemgetter((y, x)), data[1]),
#         color=col
#     )
#     plt.pause(0.03)
        
map(
    lambda idx, ax: plt.colorbar(
        month_plots[0][idx],
        ax=ax
    ),
    zip([1, 2, 3], [ax1, ax2, ax3]),
)

def im_visible(n_float):
    global current
    n = int(round(n_float))
    if n == current:
        return
    map(set_visible_false, month_plots[current])
    current = n
    map(set_visible_true, month_plots[current])
    map(lambda a: a.set_title(str(n)), axs)

click_coord = None
def on_click(event):
    global click_coord
    # get the x and y coords, flip y from top to bottom
    x, y = event.x, event.y
    if event.button==1:
        if event.inaxes is not None:
            click_coord = (x, y)

def on_release(event):
    global click_cooord
    x, y = event.x, event.y
    if event.button==1:
        if event.inaxes is not None and click_coord == (x, y):
            print ('data coords %f %f' % (event.xdata, event.ydata))
            plot_graphs(int(x), int(y), ax4)
            plt.pause(0.05)

plt.connect('button_press_event', on_click)
plt.connect('button_release_event', on_release)
sl = mpl.widgets.Slider(
    plt.axes([0.1, 0.03, 0.8, 0.02]),
    'month',
    0, len(month_plots)-1,
    valinit=0
)
sl.on_changed(im_visible)
plot_graphs(1480, 225, ax4)
map(
    lambda x: map(set_visible_false, x),
    month_plots[1:],
)
plt.gcf().show()
raw_input('Press any key to return')

