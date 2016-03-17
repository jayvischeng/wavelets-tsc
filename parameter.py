import pywt
import pandas as pd
from os.path import join
from os import listdir
from os.path import isfile, join
import os


def get_folders(path):
    return [join(path, f) for f in listdir(path) if not isfile(join(path, f))]


if __name__ == '__main__':
	for family in pywt.families():
	    for wavelet_name in pywt.wavelist(family)[-1:]:
	        for folder in get_folders('NewlyAddedDatasets/'):
	            df = pd.DataFrame.from_csv(join(folder, 'test.csv'), index_col=False)
	            nrows, _ = df.shape
	            x = 0
	            while x <= nrows:
	                print "'%s' '%s' '%s' '%s'" % (folder, wavelet_name, x, x + 300)
	                x += 300
