import numpy as np
import pandas as pd
import cPickle

from TIAM.config import WHICH_EXP, WHICH_METHOD
from TIAM.analysis import load_data
from TIAM.analysis import load_classifier
from TIAM.analysis.classifier_setup import classifier_setup_labeled, classifier_setup_unlabeled
import warnings

def classify(labeled=False,all_class=False):
    if labeled:
        warnings.warn("Labeled data classified as part of training")
	x, xs, x_scaled, y = classifier_setup_labeled()
    else:
	x, xs, x_scaled = classifier_setup_unlabeled()
    hmmc = load_classifier.hmmc()
    svmc = load_classifier.svmc()
    dtreec = load_classifier.dtreec()
    gbtreec = load_classifier.gbtreec()

    Y_hmm = [hmmc.decode(x)[1] for x in xs]
    Y_hmm = pd.DataFrame(np.concatenate(Y_hmm)[:,None], columns=['labels'])
    cPickle.dump(Y_hmm, open('../out/{0}/Y_hmm.pk'.format(WHICH_EXP), 'w'))

    Y_svm = svmc.predict(x_scaled)
    Y_svm = pd.DataFrame(Y_svm[:,None], columns=['labels'])
    cPickle.dump(Y_svm, open('../out/{0}/Y_svm.pk'.format(WHICH_EXP), 'w'))

    Y_dtree = dtreec.predict(x)
    Y_dtree = pd.DataFrame(Y_dtree[:,None],columns=['labels'])
    cPickle.dump(Y_dtree, open('../out/{0}/Y_dtree.pk'.format(WHICH_EXP), 'w'))

    Y_gbtree = gbtreec.predict(x)
    Y_gbtree = pd.DataFrame(Y_gbtree[:,None], columns=['labels'])
    cPickle.dump(Y_gbtree, open('../out/{0}/Y_gbtree.pk'.format(WHICH_EXP), 'w'))

    # cPickle.dump(vars()['Y_{0}'.format(WHICH_METHOD)],
    #     	open('../out/{0}/Y_predicted.pk'.format(WHICH_EXP), 'w'))
