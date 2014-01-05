import scipy.io

from TIAM.config import WHICH_EXP, WHICH_METHOD
from TIAM.analysis import load_data

#exec 'load_data.Y_{0}()'.format(WHICH_METHOD)

Y = load_data.Y_svm()

scipy.io.savemat('../out/{0}/Y_svm'.format(WHICH_EXP),Y.labels.to_dict())
