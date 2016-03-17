#! /usr/bin/python
import pandas as pd
import sys
from fastdtw import fastdtw
from sklearn.neighbors import KNeighborsClassifier
from os.path import join


def distance_func(s1, s2):
    return float(fastdtw(s1, s2)[0])


def fastdtw_knn(folder, start, end, k=1):
    neigh = KNeighborsClassifier(n_neighbors=k, metric='pyfunc', func=distance_func)
    traindf = pd.DataFrame.from_csv(join(folder, 'train.csv'), index_col=False)
    X = traindf.iloc[:, 1:].values.tolist()
    y = traindf.iloc[:, 0].values.tolist()
    neigh.fit(X, y)
    testdf = pd.DataFrame.from_csv(join(folder, 'test.csv'), index_col=False)
    testdf = testdf.iloc[start:end, :]
    X1 = testdf.iloc[:, 1:].values.tolist()
    labelled = testdf.iloc[:, 0].values.tolist()
    predicted = neigh.predict(X1)
    rdf = pd.DataFrame({'label': labelled, 'predicted': predicted})
    rdf.to_csv(join(folder, 'fastdtw_prediction_raw_%s_%s.csv' % (start, end)), index=False)

    return


if __name__ == '__main__':
    fastdtw_knn(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]))
