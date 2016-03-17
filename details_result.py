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
#     print folder
    raw = 0
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
            dfD = pd.concat(dfDs)
            dfD.to_csv(join(folder, 'fastdtw_prediction_%s_cD.csv' % wavelet_name), index=False)
            cd = 100.0 * dfD[dfD['label'] == dfD['predicted']].shape[0] / dfD.shape[0]
            row[wavelet_name] = cd
            if cd >= raw:
                print '&', '{\\bf', '{0:.1f}'.format(cd), '}',
            else:
                print '&', '{0:.1f}'.format(cd),
    print '\\\\'
    rows.append(row)
    i += 1
pd.DataFrame(rows).to_csv('NewlyAddedDatasets/wavelet_details.csv', index=False)



from pylab import rcParams
import matplotlib.pyplot as plt
import matplotlib
from matplotlib.lines import Line2D
import numpy as np


markers = []
for m in Line2D.markers:
    try:
        if len(m) == 1 and m != ' ':
            markers.append(m)
    except TypeError:
        pass

styles = markers + [
    r'$\lambda$',
    r'$\bowtie$',
    r'$\circlearrowleft$',
    r'$\clubsuit$',
    r'$\checkmark$']

# print styles
colors = ('b', 'g', 'r', 'c', 'm', 'y', 'k', 'w')

rcParams['figure.figsize'] = 13.5, 3

df = pd.DataFrame.from_csv('NewlyAddedDatasets/wavelet_details.csv', index_col=False)
df = df[['Raw', 'haar', 'db20', 'sym20', 'coif5', 'bior6.8', 'rbio6.8', 'dmey']]
nrows, ncols = df.shape

# http://matplotlib.org/1.3.1/examples/pylab_examples/line_styles.html
markers = ['*', 's', 'o', '.', '^', 'D', '<', '>']
# http://stackoverflow.com/questions/22408237/named-colors-in-matplotlib
colors = ['lightskyblue', 'deepskyblue', 'lightgreen', 'darkgreen', 'crimson', 'lightsalmon', 'rosybrown', 'darkred']
fig = plt.figure()
ax = plt.subplot(111)
for i in range(ncols):
    print df.columns[i], markers[i], colors[i]
    ax.plot(range(1, 40), df.iloc[:, i], markers[i], color=colors[i], markersize=6, label=df.columns[i])

box = ax.get_position()
ax.set_position([box.x0, box.y0 + box.height * 0.1,
                 box.width, box.height * 0.9])

# Put a legend below current axis
ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.2),
          fancybox=False, shadow=False, numpoints=1, ncol=8)
ax.xaxis.set_ticks(np.arange(0,40,1))
plt.xlabel('Dataset')
plt.ylabel('Accuracy (percentage)')
plt.show()



df = pd.DataFrame.from_csv('NewlyAddedDatasets/wavelet_details.csv', index_col=False)
del df['dataset']

df.rank(axis=1)


from pylab import rcParams
import matplotlib.pyplot as plt
import matplotlib
pd.options.display.mpl_style = 'default'
pd.options.display.mpl_style = None

rcParams['figure.figsize'] = 7.5, 3
fig = plt.figure()
ax = df[['Raw', 'haar', 'db20', 'sym20', 'coif5', 'bior6.8', 'rbio6.8', 'dmey']].rank(axis=1, ascending=False).boxplot(fontsize=12, return_type='axes', sym='c+', grid=False)
