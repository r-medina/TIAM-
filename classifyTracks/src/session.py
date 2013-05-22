import numpy as np
import pickle
from sklearn import hmm

# features
X = pickle.load(open('X.pk', 'r'))
# labels
Y = pickle.load(open('Y.pk', 'r'))

# clip range for each feature
clip = {'straightness': [-0.5, 1.0],
        'bending': [-0.5, 0.5],
        'efficiency': [0., 1.], 
        'asymmetry': [0., 1.],
        'skewness': [-2., 2.],
        'kurtosis': [1., 5.],
        'displacement': [0., 15.],
        'confinement': [-12, 0.]}
for feat in clip:
    X[feat][X[feat]<clip[feat][0]] = clip[feat][0]
    X[feat][X[feat]>clip[feat][1]] = clip[feat][1]

# hmm analysis pukes if this feature is included
X = X.drop('confinement', 1)

# get list of tracks and list of labels
xs = []
ys = []
D = pd.merge(X, Y, left_index=True, right_index=True)
for n, track in D.groupby(level=0):
    y = np.array(track['labels'])
    x = np.array(track.drop('labels', 1))
    # do not include tracks where y == -1    
    msk = (y >= 0)
    if any(msk):
        xs.append(x[y >= 0])
        ys.append(y[y >= 0])

# set up hmm
model = hmm.GaussianHMM(
            # 2 states, diagonal covariance
            2, 'diag',
            # uninformative initial probability
            [0.5, 0.5],
            # transition matrix with state life time ~50 time points
            np.array([[0.98, 0.02],
                      [0.02, 0.98]]))
# train hmm
model.fit(xs)
# get states. note: this is a list, containing all tracks where y!=-1
y_hmm = [model.decode(x)[1] for x in xs]


# run SVM analysis
from sklearn import preprocessing, svm, metrics, cross_validation
x = np.concatenate(xs, 0)
y = np.concatenate(ys, 0)
kfold = cross_validation.StratifiedKFold(y,10)
svc = svm.SVC()
performance = cross_validation.cross_val_score(svc, x_scaled, y, cv=kfold, n_jobs=-1)
svc.fit(x_scaled, y)
# note: this is length 8800, all tracks concatenated
y_svc = svc.predict(x_scaled)
