import pywt
import pandas as pd
from os.path import join
from os import listdir
from os.path import isfile, join
import os


def get_folders(path):
    return [join(path, f) for f in listdir(path) if not isfile(join(path, f))]


def transform_dataframe(wavelet, df, outf1, outf2):
    nrows, ncols = df.shape
    sample_size = ncols - 1
    half = sample_size / 2 + sample_size % 2
    cols = ['label']
    for i in range(half):
        cols.append('col%d' % i)
    nvA = []
    nvD = []
    for i in range(nrows):
        values = df.iloc[i, 1:].values.tolist()
        vA = {}
        vD = {}
        vA['label'] = int(df.iloc[i, 0])
        vD['label'] = int(df.iloc[i, 0])
        cA, cD = pywt.dwt(values, wavelet)
        for i in range(half):
            vA['col%d' % i] = cA[i]
            vD['col%d' % i] = cD[i]
        nvA.append(vA)
        nvD.append(vD)
    pd.DataFrame(nvA, columns=cols).to_csv(outf1, index=False)
    pd.DataFrame(nvD, columns=cols).to_csv(outf2, index=False)
    return


def dwt_transform(folder, wavelet):
    wtname = wavelet.name
    testdf = pd.DataFrame.from_csv(join(folder, 'test.csv'), index_col=False)
    transform_dataframe(wavelet, testdf, join(folder, 'test_%s_cA.csv' % wtname), join(folder, 'test_%s_cD.csv' % wtname))
    traindf = pd.DataFrame.from_csv(join(folder, 'train.csv'), index_col=False)
    transform_dataframe(wavelet, traindf, join(folder, 'train_%s_cA.csv' % wtname), join(folder, 'train_%s_cD.csv' % wtname))
    return


def dwt_transform_all(path, wavelet):
    for folder in get_folders(path):
        dwt_transform(folder, wavelet)
    return


if __name__ == '__main__':
    for family in pywt.families():
        for wavelet_name in pywt.wavelist(family):
            wavelet = pywt.Wavelet(wavelet_name)
            dwt_transform_all('NewlyAddedDatasets', wavelet)
