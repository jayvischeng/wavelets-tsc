import pywt
import pandas as pd
from os.path import join
from os import listdir
from os.path import isfile, join
import os


def transform_dataframe(wavelet_name, df, level, prefix):
    nrows, ncols = df.shape
    out = {}
    for i in range(level + 1):
        out[i] = []
    for i in range(nrows):
        values = df.iloc[i, 1:].values.tolist()
        dec = pywt.wavedec(values, wavelet_name, level=level)
        for j in range(level+1):
            row = {'label': int(df.iloc[i, 0])}
            for k in range(len(dec[j])):
                row['col%d' % k] = dec[j][k]
            out[j].append(row)
    for i in range(level + 1):
        cols = ['label']
        for j in range(len(out[i][0].keys()) - 1):
            cols.append('col%s' % j)
        pd.DataFrame(out[i], columns=cols).to_csv('%s_%s_%d_%d.csv' % (prefix, wavelet_name, level, i), index=False)
    return

# df = pd.DataFrame.from_csv('NewlyAddedDatasets/ArrowHead/test.csv', index_col=False)
# transform_dataframe('sym20', df, 2, 'NewlyAddedDatasets/ArrowHead/AAA/test')
# transform_dataframe('sym20', df, 1, 'NewlyAddedDatasets/ArrowHead/AAA/test')

def get_folders(path):
    return [join(path, f) for f in listdir(path) if not isfile(join(path, f))]


for folder in get_folders('NewlyAddedDatasets/'):
    testdf = pd.DataFrame.from_csv(join(folder, 'test.csv'), index_col=False)
    traindf = pd.DataFrame.from_csv(join(folder, 'train.csv'), index_col=False)
#     print folder,
    l = testdf.shape[1] - 1
    wavelet_name = 'sym20'
    for level in range(1, pywt.dwt_max_level(l, pywt.Wavelet('sym20')) + 1):
        print folder, wavelet_name, level
        transform_dataframe(wavelet_name, testdf, level, join(folder, 'test'))
        transform_dataframe(wavelet_name, traindf, level, join(folder, 'train'))
