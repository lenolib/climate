from __future__ import print_function, division

import pandas as pd
import numpy as np
import matplotlib as mpl
from matplotlib import pyplot as plt


plt.figure(figsize=(20,10));
arr = np.load('./worldclim/mip_8/bio_12_mip8.npz')['arr_0']
ax = plt.imshow(
    arr,
    cmap=mpl.cm.Paired,
    vmin=0,
    vmax=4000,
)
plt.colorbar(fraction=0.03, shrink=0.65)
plt.title('Annual precipitation [mm], source: WorldClim')
ax.axes.xaxis.set_visible(False)
ax.axes.yaxis.set_visible(False)
plt.subplots_adjust(0.02,0.02, 0.98, 0.98)

if raw_input("Save figure? [y/n]").lower() == 'y':
    plt.gcf().savefig('./precipitation_annual.png', dpi=240)

plt.show()
