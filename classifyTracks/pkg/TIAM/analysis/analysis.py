import numpy as np
import pandas as pd
import pickle
from sklearn import preprocessing, svm, hmm, tree, ensemble, metrics, cross_validation
import matplotlib.pyplot as plt

from TIAM.load_data import X, Y
from TIAM.config import WHICH_EXP

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
D = pd.merge(X, Y, left_index=True, right_index=True)
# note: this screws up hierarchical indexing
for n, track in D.groupby(level=0):
    x = np.array(track.drop('labels', 1))
    y = np.array(track['labels'])
    # do not include tracks where y == -1    
    msk = (y >= 0)
    if any(msk):
        xs.append(x[y >= 0])
        ys.append(y[y >= 0])
    else:
        pass

x = np.concatenate(xs, 0)
y = np.concatenate(ys, 0)
Y_proc = pd.DataFrame(y[:,None], columns=['labels'])
pickle.dump(Y_proc, open('../out/{0}/Y_proc.pk'.format(WHICH_EXP), 'w'))

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
Y_hmm = pd.DataFrame(np.concatenate(y_hmm)[:,None],index=Y_proc.index, columns=['labels'])
pickle.dump(Y_hmm, open('../out/{0}/Y_hmm.pk'.format(WHICH_EXP), 'w'))

# run SVM analysis
x = np.concatenate(xs, 0)
x_scaled = preprocessing.scale(x)
y = np.concatenate(ys, 0)
kfold = cross_validation.StratifiedKFold(y,10)
svc = svm.SVC()
svc.fit(x_scaled, y)
# note: this is length 8800, all tracks concatenated
y_svm = svc.predict(x_scaled)
#Y_svm = pd.DataFrame(y_svm[:,None],index=Y.index, columns=['labels'])
Y_svm = pd.DataFrame(y_svm[:,None], columns=['labels'])
pickle.dump(Y_svm, open('../out/{0}/Y_svm.pk'.format(WHICH_EXP), 'w'))

# run basic decision trees
dtree = tree.DecisionTreeClassifier(criterion='entropy', min_samples_leaf=50, max_depth=3, compute_importances=True)
performance = cross_validation.cross_val_score(dtree, x, y, cv=kfold, n_jobs=-1)
print 'decision tree performance (mean, stdev) under 10-fold CV:'
print performance.mean(), performance.std()

dtree.fit(x, y)
print pd.DataFrame(dtree.feature_importances_, columns=['Importance'], index=X.columns).sort(['Importance'], ascending=False)
tree.export_graphviz(dtree, out_file='../out/{0}/dtree.dot'.format(WHICH_EXP), feature_names=X.columns)

#run gradient boosting ensemble
gbtree = ensemble.GradientBoostingClassifier(n_estimators=100, learning_rate=1.0, max_depth=5, random_state=0)
performance = cross_validation.cross_val_score(gbtree, x, y, cv=kfold, n_jobs=-1)
print 'gradient boosting ensemble performance (mean, stdev) under 10-fold CV:'
print performance.mean(), performance.std()

gbtree.fit(x,y)
feature_importance = gbtree.feature_importances_
feature_importance = 100.0 * (feature_importance / feature_importance.max())
sorted_idx = np.argsort(feature_importance)
pos = np.arange(sorted_idx.shape[0]) + .5

plt.figure(figsize=(12, 6))
plt.subplot(1, 1, 1)
plt.barh(pos, feature_importance[sorted_idx], align='center')
plt.yticks(pos, X.columns[sorted_idx])
plt.xlabel('Relative Importance')
plt.title('Variable Importance')
plt.show()
