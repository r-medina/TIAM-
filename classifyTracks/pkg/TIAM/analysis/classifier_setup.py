import numpy as np
import pandas as pd
from sklearn import preprocessing
import pickle

from TIAM.config import WHICH_EXP
from TIAM.analysis import load_data


X = load_data.X()
Y = load_data.Y()
# clip range for each feature
clip = {'straightness': [-1.0, 1.0],
	'bending': [-0.5, 0.5],
	'efficiency': [0., 0.2], 
	'asymmetry': [0., 1.],
	'skewness': [-2., 2.],
	'kurtosis': [1., 5.],
	'displacement': [0., 20.],
	'confinement': [-2, 2.]}
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
	else:
		pass

multi = pd.MultiIndex.from_tuples(pairs, names=['track', 'frame'])
y = np.concatenate(ys, 0)
# essentially the same as y, but has hierarchical indexing
Y_supervised = pd.DataFrame(y[:,None], index=multi, columns=['labels'])
pickle.dump(Y_supervised, open('../out/{0}/Y_supervised.pk'.format(WHICH_EXP), 'w'))

x = np.concatenate(xs, 0)
x_scaled = preprocessing.scale(x)
