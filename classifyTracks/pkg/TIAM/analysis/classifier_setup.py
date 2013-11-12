import numpy as np
import pandas as pd
from sklearn import preprocessing
import cPickle

from TIAM.config import WHICH_EXP
from TIAM.analysis import load_data

clip = {'straightness': [-1.0, 1.0],
        'bending': [-0.5, 0.5],
        'efficiency': [0., 0.2],
        'asymmetry': [0., 1.],
        'skewness': [-2., 2.],
        'kurtosis': [1., 5.],
        'displacement': [0., 20.],
        'confinement': [-2, 2.]}

def classifier_setup_labeled():
    X = load_data.X()
    Y = load_data.Y_supervised()
    # clip range for each feature
    for feat in clip:
        X[feat][X[feat]<clip[feat][0]] = clip[feat][0]
        X[feat][X[feat]>clip[feat][1]] = clip[feat][1]

    # get list of tracks and list of labels
    xs = []
    ys = []
    pairs = []
    D = pd.merge(X, Y, left_index=True, right_index=True)
    for n, track in D.groupby(level=0):
    	x = np.array(track.drop('labels', 1))
    	y = np.array(track['labels'])
    	# do not include tracks where y == -1    
    	msk = (y >= 0)
    	if any(msk):
    	    xs.append(x[msk])
    	    ys.append(y[msk])
    	    # preserves hierarchical indexing after tracks where
    	    # y == -1 are removed
    	    for pair in track.index.tolist():
                pairs.append(pair)

    x = np.concatenate(xs, 0)
    y = np.concatenate(ys, 0)
    Y_proc = pd.DataFrame(y[:,None], columns=['labels'])
    cPickle.dump(Y_proc, open('../out/{0}/Y_proc.pk'.format(WHICH_EXP), 'w'))

    multi = pd.MultiIndex.from_tuples(pairs, names=['track', 'frame'])
    # essentially the same as y, but has hierarchical indexing
    Y_supervised = pd.DataFrame(y[:,None], index=multi, columns=['labels'])
    cPickle.dump(Y_supervised, open('../out/{0}/Y_supervised.pk'.format(WHICH_EXP), 'w'))
    
    x_scaled = preprocessing.scale(x)
    return x, xs, x_scaled, y


def classifier_setup_unlabeled():
    X = load_data.X()
    # clip range for each feature
    for feat in clip:
        X[feat][X[feat]<clip[feat][0]] = clip[feat][0]
        X[feat][X[feat]>clip[feat][1]] = clip[feat][1]

    # get list of tracks and list of labels
    xs = []
    pairs = []
    for n, track in X.groupby(level=0):
        x = np.array(track)
        xs.append(x)

    x = np.concatenate(xs, 0)
    x_scaled = preprocessing.scale(x)
    return x, xs, x_scaled
