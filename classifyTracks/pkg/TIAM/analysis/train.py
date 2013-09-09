import numpy as np
import pandas as pd
import pickle
from sklearn import preprocessing, svm, hmm, tree, ensemble, metrics, cross_validation
import matplotlib.pyplot as plt

from TIAM.config import WHICH_EXP
from TIAM.analysis.classifier_setup import classifier_setup_labeled

def train(labeled=False):
    assert labeled, 'Cannot train on unlabeled data'

    xs, x_scaled, y = classifier_setup_labeled()

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
    pickle.dump(hmmc, open('../out/{0}/hmmc.pk'.format(WHICH_EXP), 'w'))

    # run SVM analysis
    #kfold = cross_validation.StratifiedKFold(y,10)
    svmc = svm.SVC()
    svmc.fit(x_scaled, y)
    pickle.dump(svmc, open('../out/{0}/svmc.pk'.format(WHICH_EXP), 'w'))
