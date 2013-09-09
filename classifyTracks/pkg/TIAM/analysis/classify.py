import numpy as np
import pandas as pd
import pickle

from TIAM.config import WHICH_EXP, WHICH_METHOD
from TIAM.analysis import load_data
from TIAM.analysis import load_classifier

def classify(labeled=False):
    from TIAM.analysis.classifier_setup import xs, x_scaled
    hmmc = load_classifier.hmmc()
    svmc = load_classifier.svmc()
    y_hmm = [hmmc.decode(x)[1] for x in xs]
    Y_hmm = pd.DataFrame(np.concatenate(y_hmm)[:,None], columns=['labels'])
    Y_hmm = (Y_hmm-1)*-1
    pickle.dump(Y_hmm, open('../out/{0}/Y_hmm.pk'.format(WHICH_EXP), 'w'))

    y_svm = svmc.predict(x_scaled)
    Y_svm = pd.DataFrame(y_svm[:,None], columns=['labels'])
    pickle.dump(Y_svm, open('../out/{0}/Y_svm.pk'.format(WHICH_EXP), 'w'))

    pickle.dump(vars()['Y_{0}'.format(WHICH_METHOD)],
		open('../out/{0}/Y_predicted.pk'.format(WHICH_EXP), 'w'))
