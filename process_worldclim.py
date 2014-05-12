from __future__ import print_function, division

import os
import pandas as pd
import numpy as np
import glob
import matplotlib as mpl
from matplotlib import pyplot as plt
from itertools import imap
from scipy.misc import imresize

worldclim_catalog = './worldclim'
sizes = [4, 8, 16]

def resize(arr, numerator, interp):
    a = arr[::numerator, ::numerator].astype(np.float32)
    a[a==-9999] = np.nan
    
    return a


def mipmap(arr, numerators, interp='nearest'):
    resizes = imap(
        lambda numerator: (
            numerator,
            resize(arr, numerator, interp=interp),
        ),
        numerators,
    )
    print('Mipmapped array')
    return resizes


def save(path, name, arr):
    if not os.path.exists(path):
        os.makedirs(path)
    fpath = os.path.join(path,name)
    np.savez_compressed(fpath, arr)
    print('Wrote', fpath)

os.chdir(worldclim_catalog)
files = glob.glob('*.bil')
if not files:
    raise Exception("Could not find any bil-files in {}".format(
        os.path.abspath(os.curdir)
    ))
proceed = raw_input(
    "This will read and downsize {f1} ... {f2} by {sizes} times "
    "and put results in a subfolders 'mip*'. Proceed? [y/n]".format(
        f1=files[:1],
        f2=files[-1:],
        sizes=sizes,
    )
)
if proceed.lower() == 'y':
    for f in files:
        arr = np.fromfile(f, dtype=np.int16).reshape(-1,43200)
        print('Read', f)
        stem = os.path.split(os.path.splitext(f)[0])[1]
        map(
            lambda (numerator, arr): save(
                'mip_{}'.format(numerator),
                '{stem}_mip{mip}'.format(stem=stem, mip=numerator),
                arr,
            ),
            mipmap(arr, sizes)
        )
else:
    print('Exiting')