from scipy.io import loadmat
import pandas as pd
from os import listdir
from os.path import isfile, join
import os


def get_folders(path):
    return [join(path, f) for f in listdir(path) if not isfile(join(path, f))]


def get_files(path, ft='.mat'):
    return [join(path, f) for f in listdir(path) if f.endswith(ft) and isfile(join(path, f))]


def convert_to_csv(folder):
    files = get_files(folder, ft='.mat')
    for f in files:
        print f
        mat = loadmat(f)
        testdir = join(folder, 'test')
        traindir = join(folder, 'train')
        if not os.path.exists(testdir):
            os.makedirs(testdir)
        if not os.path.exists(traindir):
            os.makedirs(traindir)
        for k in mat.keys():
            if 'test' in k.lower():
                df = pd.DataFrame(mat[k])
                df.to_csv(join(folder, 'test.csv'), index=False)
            if 'train' in k.lower():
                df = pd.DataFrame(mat[k])
                df.to_csv(join(folder, 'train.csv'), index=False)
    return


def convert_all(path):
    for folder in get_folders(path):
        convert_to_csv(folder)
    return


if __name__ == '__main__':
    convert_all('NewlyAddedDatasets')
