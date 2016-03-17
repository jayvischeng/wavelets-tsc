import pywt
import pandas as pd
from os.path import join
from os import listdir
from os.path import isfile, join
import os


def get_folders(path):
    return [join(path, f) for f in listdir(path) if not isfile(join(path, f))]



dn = 0
for folder in get_folders('NewlyAddedDatasets/'):
    print dn + 1,
    raw = 0
    try:
        df = pd.DataFrame.from_csv(join(folder, 'fastdtw_prediction_db1.csv'), index_col=False)
        raw = 100.0 * df[df['label'] == df['original_data']].shape[0] / df.shape[0]
#         print "{0:.1f}".format(raw),
    except:
        df = pd.DataFrame.from_csv(join(folder, 'fastdtw_prediction_raw.csv'), index_col=False)
        raw = 100.0 * df[df['label'] == df['predicted']].shape[0] / df.shape[0]
#         print "{0:.1f}".format(raw),
    print '&', "{0:.1f}".format(raw),
    df = pd.DataFrame.from_csv(join(folder, 'test.csv'), index_col=False)
    nrows, ncols = df.shape
    ncols -= 1
#     print ncols
    wavelet_name = 'sym20'
    for level in range(2, 7):
        if level > pywt.dwt_max_level(ncols, pywt.Wavelet('sym20')):
            print '& &',
            continue
        dfps = []
        x = 0
        while x < nrows:
            dfp = pd.DataFrame.from_csv(
                join(folder, 'fastdtw_prediction_%s_%s_%s_%s_%s.csv' % (wavelet_name, level, 0, x, x + 301)),
                index_col=False
            )
            x += 301
            dfps.append(dfp)
        dfps = pd.concat(dfps)
        dfps.to_csv(join(folder, 'fastdtw_prediction_%s_%s_%s.csv' % (wavelet_name, level, 0)), index=False)
        acc = 100.0 * dfps[dfps['label'] == dfps['predicted']].shape[0] / dfps.shape[0]
        nncols = pd.DataFrame.from_csv(join(folder, 'test_sym20_%s_%s.csv' % (level, 0)), index_col=False).shape[1] - 1
#         print level, nncols, "{0:.1f}".format(100.0*(ncols - nncols)/ncols), "{0:.1f}".format(acc)
        print '&', "{0:.1f}".format(100.0*(ncols - nncols)/ncols), '&', 
        if acc >= raw:
            print '{\\bf', "{0:.1f}".format(acc), '}',
        else:
            print "{0:.1f}".format(acc),
    print '\\\\'
    dn += 1
