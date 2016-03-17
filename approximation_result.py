import pywt
import pandas as pd
from os.path import join
from os import listdir
from os.path import isfile, join
import os


def get_folders(path):
    return [join(path, f) for f in listdir(path) if not isfile(join(path, f))]


print '{\\bf \\#} & {\\bf Raw}',
for family in pywt.families():
    for wavelet_name in pywt.wavelist(family)[-1:]:
        print '& {\\bf', wavelet_name, '}',
print '\\\\'
print '\\midrule'

rows = []
i = 0
for folder in get_folders('NewlyAddedDatasets/'):
    print i + 1,
    print '&',
    row = {"dataset": i + 1}

    try:
        df = pd.DataFrame.from_csv(join(folder, 'fastdtw_prediction_db1.csv'), index_col=False)
        raw = 100.0 * df[df['label'] == df['original_data']].shape[0] / df.shape[0]
        print "{0:.1f}".format(raw),
    except:
        df = pd.DataFrame.from_csv(join(folder, 'fastdtw_prediction_raw.csv'), index_col=False)
        raw = 100.0 * df[df['label'] == df['predicted']].shape[0] / df.shape[0]
        print "{0:.1f}".format(raw),
    row['Raw'] = raw
    for family in pywt.families():
        for wavelet_name in pywt.wavelist(family)[-1:]:
            df = pd.DataFrame.from_csv(join(folder, 'test.csv'), index_col=False)
            nrows, _ = df.shape
            dfAs = []
            dfDs = []
            x = 0
            while x < nrows:
                dfA = pd.DataFrame.from_csv(
                    join(folder, 'fastdtw_prediction_%s_cA_%s_%s.csv' % (wavelet_name, x, x + 300)),
                    index_col=False
                )
                dfD = pd.DataFrame.from_csv(
                    join(folder, 'fastdtw_prediction_%s_cD_%s_%s.csv' % (wavelet_name, x, x + 300)),
                    index_col=False
                )
                dfAs.append(dfA)
                dfDs.append(dfD)
                x += 300
            dfA = pd.concat(dfAs)
            dfA.to_csv(join(folder, 'fastdtw_prediction_%s_cA.csv' % wavelet_name), index=False)
            ca = 100.0 * dfA[dfA['label'] == dfA['predicted']].shape[0] / dfA.shape[0]
            if ca >= raw:
                print '&', '{\\bf', '{0:.1f}'.format(ca), '}',
            else:
                print '&', '{0:.1f}'.format(ca),
            row[wavelet_name] = ca
    print '\\\\'
    rows.append(row)
    i += 1
pd.DataFrame(rows).to_csv('NewlyAddedDatasets/wavelet_approx.csv', index=False)


df = pd.DataFrame.from_csv('NewlyAddedDatasets/wavelet_approx.csv', index_col=False)
del df['dataset']
df.rank(axis=1)


from pylab import rcParams
import matplotlib.pyplot as plt
import matplotlib
pd.options.display.mpl_style = 'default'
pd.options.display.mpl_style = None

rcParams['figure.figsize'] = 7.5, 3
fig = plt.figure()
df[['Raw', 'haar', 'db20', 'sym20', 'coif5', 'bior6.8', 'rbio6.8', 'dmey']].rank(axis=1)
ax = df[['Raw', 'haar', 'db20', 'sym20', 'coif5', 'bior6.8', 'rbio6.8', 'dmey']].rank(axis=1, ascending=False).boxplot(fontsize=12, return_type='axes', sym='c+', grid=False)
