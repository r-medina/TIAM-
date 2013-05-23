import numpy as np
import pandas as pd
import pickle
from sklearn import preprocessing, svm, hmm, metrics, cross_validation

# features
X = pickle.load(open('../out/X.pk', 'r'))
# labels
Y = pickle.load(open('../out/Y.pk', 'r'))

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

# hmm analysis pukes if this feature is included
#X = X.drop('confinement', 1)

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
    else:
        print n 

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
Y_hmm = pd.DataFrame(np.concatenate(y_hmm)[:,None],index=Y.index, columns=['labels'])
pickle.dump(Y_hmm, open('../out/Y_hmm.pk', 'w'))
print y_hmm

# run SVM analysis
x = np.concatenate(xs, 0)
x_scaled = preprocessing.scale(x)
y = np.concatenate(ys, 0)
kfold = cross_validation.StratifiedKFold(y,10)
svc = svm.SVC()
performance = cross_validation.cross_val_score(svc, x_scaled, y, cv=kfold, n_jobs=-1)
svc.fit(x_scaled, y)
# note: this is length 8800, all tracks concatenated
y_svm = svc.predict(x_scaled)
Y_svm = pd.DataFrame(y_svm[:,None],index=Y.index, columns=['labels'])
pickle.dump(Y_svm, open('../out/Y_svm.pk', 'w'))
