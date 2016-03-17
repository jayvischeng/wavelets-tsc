import pywt
import pandas as pd
from os.path import join
from os import listdir
from os.path import isfile, join
import os

def get_folders(path):
    return [join(path, f) for f in listdir(path) if not isfile(join(path, f))]

wavelet_name = 'sym20'
for folder in get_folders('NewlyAddedDatasets/'):
    df = pd.DataFrame.from_csv(join(folder, 'test.csv'), index_col=False)
    nrows, ncols = df.shape
    for level in range(1, pywt.dwt_max_level(ncols-1, pywt.Wavelet('sym20')) + 1):
        for i in range(level + 1):
            x = 0
            while x <= nrows:
                print "'%s' '%s' '%s' '%s' '%s' '%s'" % (folder, wavelet_name, level, i, x, x + 301)
                x += 301