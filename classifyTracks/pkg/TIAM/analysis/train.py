import numpy as np
import pandas as pd
import cPickle
from sklearn import preprocessing, svm, hmm, tree, ensemble, metrics, cross_validation
import matplotlib.pyplot as plt

from TIAM.config import WHICH_EXP
from TIAM.analysis.classifier_setup import classifier_setup_labeled
from TIAM.analysis.classify import classify
from TIAM.analysis.test_results import test_results

def train(labeled=False):
    assert labeled, 'Cannot train on unlabeled data'
    
    x, xs, x_scaled, y = classifier_setup_labeled()
    kfold = cross_validation.StratifiedKFold(y,10)

    # set up hmm
    hmmc = hmm.GaussianHMM(
        # 2 states, diagonal covariance
        2, 'diag',
        # uninformative initial probability
        [0.5, 0.5],
        # transition matrix with state life time ~50 time points
        np.array([[0.98, 0.02],
                  [0.02, 0.98]]))
    # train hmm
    hmmc.fit(xs)
    cPickle.dump(hmmc, open('../out/{0}/hmmc.pk'.format(WHICH_EXP), 'w'))

    # run SVM analysis
    svmc = svm.SVC(probability=True)
    svmperf = cross_validation.cross_val_score(svmc, x_scaled, y, cv=kfold, n_jobs=-1)
    cPickle.dump(svmperf, open('../out/{0}/svmperf.pk'.format(WHICH_EXP), 'w'))
    svmc.fit(x_scaled,y)
    cPickle.dump(svmc, open('../out/{0}/svmc.pk'.format(WHICH_EXP), 'w'))

    # basic decision tree
    dtreec = tree.DecisionTreeClassifier(criterion='entropy',
                                        min_samples_leaf=50,
                                        max_depth=3)
    dtreeperf = cross_validation.cross_val_score(dtreec,x,y,cv=kfold,n_jobs=-1)
    cPickle.dump(dtreeperf,open('../out/{0}/dtreeperf.pk'.format(WHICH_EXP), 'w'))
    dtreec.fit(x,y)
    cPickle.dump(dtreec,open('../out/{0}/dtreec.pk'.format(WHICH_EXP), 'w'))

    #run gradient boosting ensemble
    gbtreec = ensemble.GradientBoostingClassifier(n_estimators=100,
                                                 learning_rate=1.0,
                                                 max_depth=5,
                                                 random_state=0)
    gbtreeperf = cross_validation.cross_val_score(gbtreec,x,y,cv=kfold,n_jobs=-1)
    cPickle.dump(gbtreeperf, open('../out/{0}/gbtreeperf.pk'.format(WHICH_EXP), 'w'))
    gbtreec.fit(x,y)
    cPickle.dump(gbtreec, open('../out/{0}/gbtreec.pk'.format(WHICH_EXP), 'w'))
    
    classify(labeled=True)
    test_results()
